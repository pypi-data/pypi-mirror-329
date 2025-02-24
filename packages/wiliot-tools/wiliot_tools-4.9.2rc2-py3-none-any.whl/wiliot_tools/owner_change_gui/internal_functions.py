from datetime import datetime

import databricks.sql
import pandas as pd
import json
import time
PUBLIC_VERSION = False
try:
    from wiliot_api import InternalClient, TagNotFound
except:
    PUBLIC_VERSION = True


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in: {execution_time:.4f} seconds")
        return result

    return wrapper


def get_databricks_config():
    try:
        config_path = "databricks_config.json"
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Config file not found")
        return


@time_it
def check_cloud_issues(row, expected_owner_id, client):
    tag_id = row['tag_id']
    group_id = row['group_id']
    try:
        res = client.get_tag_status(tag_id, group_id)
    except TagNotFound:
        return 'TAG_NOT_EXIST_IN_CLOUD'
    if 'ownerId' not in res or 'externalId' not in res:
        return 'ERROR_GET_STATUS_API'
    if res['ownerId'] != expected_owner_id:
        return f'OWNER_ID_IS_{res["ownerId"]}'
    if row['external_id'] != res['externalId']:
        return f'SERIALIZATION_ISSUE'
    return "UNKNOWN"


def databricks_sql(sql_query):
    config = get_databricks_config()
    if config is None:
        return
    cluster_id = config['cluster_id']
    databricks_instance = config['databricks_instance']
    org_id = config['org_id']
    token = config['token']
    http_path = f"sql/protocolv1/o/{org_id}/{cluster_id}"
    with databricks.sql.connect(
            server_hostname=databricks_instance,
            http_path=http_path,
            access_token=token
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
    return df


@time_it
def get_all_tags(request_id):
    return databricks_sql(f"""
        with failed_ids as (
            select externalId
            from owner_change_tags_info
            where requestid = '{request_id}'
              and status = 'failed'
        ),
        failed_prefixes as (
            select distinct split(externalid, 'T')[0] as prefix
            from failed_ids
        ),
        crn_tags_info as (
        select common_run_name, external_id, tag_id, group_id, fail_bin_str
        from offline_test_tag_locations
        where common_run_name in (select common_run_name
                                    from offline_test_runs
                                    where external_id_prefix in (
                                        select prefix from failed_prefixes
                                        union 
                                        select concat('010085002786501021', prefix) from failed_prefixes
                                    )))
        select *
        from crn_tags_info
    """)

@time_it
def get_fails_ids(request_id):
    return databricks_sql(f"""
        with failed_ids as (
            select externalId
            from owner_change_tags_info
            where requestId = '{request_id}'
              and status = 'failed'
        )
        select externalId as external_id
        from failed_ids
    """)
# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


def _deconstruct_arm_id(arm_id):
    parts = arm_id.split("/")
    sub_id = parts[2]
    rg_name = parts[4]
    resource_name = parts[-1]
    return sub_id, rg_name, resource_name


def _get_redis_connection_string(arm_id, credential):
    from azure.mgmt.redis import RedisManagementClient

    subscription_id, resource_group, resource = _deconstruct_arm_id(arm_id)
    management_client = RedisManagementClient(credential=credential, subscription_id=subscription_id)
    instance_response = management_client.redis.get(resource_group, resource)
    keys_response = management_client.redis.list_keys(resource_group, resource)

    instance_dict = instance_response.as_dict()
    keys_dict = keys_response.as_dict()

    host = instance_dict["host_name"]
    port = instance_dict["ssl_port"]
    password = keys_dict["primary_key"]
    return f"rediss://:{password}@{host}:{port}/0"


def _get_redis_client(redis_arm_id, credential):
    from redis import Redis

    connection_string = _get_redis_connection_string(redis_arm_id, credential)
    return Redis.from_url(connection_string)


class RedisClientPool(object):
    def __init__(self, redis_resource_ids, credential):
        self.clients = {
            redis_resource_id: _get_redis_client(redis_resource_id, credential)
            for redis_resource_id in redis_resource_ids
        }

    def get_client(self, redis_resource_id):
        return self.clients[redis_resource_id]

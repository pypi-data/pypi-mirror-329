from cdh_lava_core.databricks_service.dbx_rest import ApiClient
from cdh_lava_core.databricks_service.dbx_rest.permissions.crud import PermissionsCrud

__all__ = ["Pools"]


class Pools(PermissionsCrud):
    valid_permissions = ["CAN_MANAGE", "CAN_ATTACH_TO"]

    def __init__(self, client: ApiClient):
        super().__init__(client, "2.0/permissions/instance-pools", "instance_pool")

from cdh_lava_core.databricks_service.dbx_rest import ApiClient
from cdh_lava_core.databricks_service.dbx_rest.permissions.crud import PermissionsCrud
from cdh_lava_core.databricks_service.dbx_rest.permissions.crud import (
    What,
    PermissionLevel,
)
import logging
from opentelemetry import trace
from opentelemetry.trace import StatusCode, Status
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import sys, os

__all__ = ["Jobs"]

# noinspection PyProtectedMember
from cdh_lava_core.databricks_service.dbx_rest.permissions.crud import (
    What,
    valid_whats,
    PermissionLevel,
)

NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
SERVICE_NAME = os.path.basename(__file__)

class Jobs(PermissionsCrud):
    valid_permissions = ["IS_OWNER", "CAN_MANAGE_RUN", "CAN_VIEW", "CAN_MANAGE"]

    def __init__(self, client: ApiClient):
        super().__init__(client, "2.0/preview/permissions/jobs", "job")
        # Initialize the logger and tracer


        config = client.config  # Assume the client has a config attribute
        data_product_id = config.get("data_product_id")
        environment = config.get("environment")

        self.tracer, self.logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

    def change_owner_user(self, job_id, new_owner_id: str):
        return self.change_owner(job_id, "user_name", new_owner_id)

    def change_owner_group(self, job_id, new_owner_id: str):
        return self.change_owner(job_id, "group_name", new_owner_id)

    def change_owner_service_principal(self, job_id, new_owner_id: str):
        return self.change_owner(job_id, "service_principal_name", new_owner_id)

    def change_owner(self, job_id, owner_type: What, owner_id: str):
        if owner_type == "user":
            owner_type = "user_name"
        if owner_type == "group":
            owner_type = "group_name"
        if owner_type == "service_principal":
            owner_type = "service_principal_name"
        assert owner_type in [
            "user_name",
            "group_name",
            "service_principal_name",
        ], f'Expected owner_type to be one of "user_name", "group_name", or "service_principal_name", found "{owner_type}".'

        old_what, old_id = self.get_owner(job_id)

        params = {
            "access_control_list": [
                {owner_type: owner_id, "permission_level": "IS_OWNER"},
                {old_what: old_id, "permission_level": "CAN_MANAGE"},
            ]
        }
        return self.client.api("PATCH", f"{self.path}/{job_id}", data=params)

    def get_owner(self, job_id):
        results = self.get(job_id)
        for access_control in results.get("access_control_list"):
            for permission in access_control.get("all_permissions"):
                if permission.get("permission_level") == "IS_OWNER":
                    if "user_name" in access_control:
                        return "user_name", access_control.get("user_name")
                    elif "group_name" in access_control:
                        return "group_name", access_control.get("group_name")
                    elif "service_principal_name" in access_control:
                        return "service_principal_name", access_control.get(
                            "service_principal_name"
                        )
                    else:
                        raise ValueError(
                            f"Could not find user, group or service principal name for job {job_id}"
                        )

    def share_job(self, job_id, share_with: What, permission_level: str, data_product_id, environment):
        """
        Shares a Databricks job with specified permissions and adds logging and tracing.

        Args:
            job_id (str): The ID of the job to share.
            share_with (What): The entity to share the job with (e.g., user or group).
            permission_level (str): The permission level (e.g., CAN_MANAGE).

        Returns:
            dict: The result of the job sharing API call.
        """
        assert permission_level in self.valid_permissions, f'Invalid permission level "{permission_level}". Must be one of {self.valid_permissions}.'
        
        # Start tracing span
        with self.tracer.start_as_current_span(f"share_job: {job_id}") as span:
            try:
                self.logger.info(f"Sharing job {job_id} with {share_with} at {permission_level} level")
                params = {
                    "access_control_list": [
                        {  "group_name": share_with,"permission_level": permission_level}
                    ]
                }
                return self.client.api("PATCH", f"{self.path}/{job_id}", data=params)
            except Exception as ex:
                error_msg = f"Error sharing job {job_id}: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                span.set_status(Status(StatusCode.ERROR, description=error_msg))
                raise

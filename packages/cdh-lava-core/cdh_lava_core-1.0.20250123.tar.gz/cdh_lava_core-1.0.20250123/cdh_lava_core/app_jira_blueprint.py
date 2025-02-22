import sys
import os
from flask_restx import Resource, fields, reqparse
import cdh_lava_core.jira_service.jira_client as jira_client
from flask_restx import Resource, fields, reqparse
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
from cdh_lava_core.az_key_vault_service import az_key_vault as cdh_az_key_vault

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))

class Issue(Resource):
    """
    Represents the endpoint for retrieving an issue related to a specific project.

    This class is used as a Flask-RESTful resource to handle requests related
    to retrieving a specific issue for a specific JIRA project.

    Args:
        Resource (type): The base class for implementing Flask-RESTful
        resources.


    Attributes:
        jira_project (str): The name or identifier of the project associated with
        the issue.
    """

    def get(self, jira_project=None, jira_issue_id=None, jira_fields=None):
        """
        Retrieves issue associated with a specific project from JIRA.

        Args:
            jira_project (str): The name or identifier of the project. If
                                not provided, retrieves issues for the default project.
            jira_issue_id (str): The identifier of the issue. If provided,
                                the method will retrieve this specific issue.
            jira_fields (str): Comma-separated string of fields to retrieve
                            for the issue(s). If not provided, defaults to
                            "summary,status,assignee".
        Returns:
            dict: A dictionary containing the retrieved issue.

        Note:
            This method communicates with JIRA to fetch the issue.

        Example: LAVA

        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span(f"issue/{jira_project}"):
            try:
                config = app.cdc_config

                cdh_databricks_kv_scope = config.get("cdh_databricks_kv_scope")

                az_kv_key_vault_name = config.get("az_kv_key_vault_name")
                data_product_id = "lava_core"
                environment = "dev"
                client_secret = config.get("client_secret")
                tenant_id = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_client_id")
                az_kv_key_vault_name = config.get("az_kv_key_vault_name")
                running_interactive = False
                if not client_secret:
                    running_interactive = True

                az_sub_web_client_secret_key = config.get(
                    "az_sub_web_client_secret_key"
                )
                obj_az_keyvault = cdh_az_key_vault.AzKeyVault(
                    tenant_id,
                    client_id,
                    client_secret,
                    az_kv_key_vault_name,
                    running_interactive,
                    data_product_id,
                    environment,
                    az_sub_web_client_secret_key,
                )

                jira_client_secret_key = config.get("jira_client_secret_key")
                jira_client_secret = obj_az_keyvault.get_secret(
                    jira_client_secret_key, cdh_databricks_kv_scope
                )
                if jira_client_secret is None:
                    raise Exception(
                        f"Unable to get Jira client secret from key_vault {jira_client_secret_key}"
                    )
                else:
                    logger.info(f"jira_client_secret_length:{len(jira_client_secret)}")
                    logger.info(
                        f"jira_client_secret_length:{str(len(jira_client_secret))}"
                    )

                if jira_project is None:
                    jira_project = "LAVA"  # Set your default jira_project value here

                jira_base_url = config.get("jira_base_url")
                jira_base_url = jira_base_url.rstrip("/")

                headers = {
                    "Authorization": f"Basic {jira_client_secret}",
                    "Content-Type": "application/json",
                }
                logger.info(f"headers:{headers}")

                params = {
                    "jql": f"project = {jira_project}",
                    "fields": ["summary", "status", "assignee"],
                }

                logger.info(f"Retrieving issue for project {jira_project}")
                logger.info(f"params: {params}")

                jira_client_instance = jira_client.JiraClient()
                jira_issue = jira_client_instance.get_issue(
                    jira_project,
                    headers,
                    jira_base_url,
                    jira_issue_id,
                    jira_fields,
                    data_product_id,
                    environment,
                )

                logger.info(jira_issue)

                return jira_issue

            except Exception as ex:
                msg = f"An unexpected error occurred: {str(ex)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
                ).force_flush()
                return {"error": f"An unexpected error occurred: {msg}"}


class Task(Resource):
    """
    Represents the endpoint for retrieving tasks related to a specific project.

    This class is used as a Flask-RESTful resource to handle requests related
    to retrieving tasks for a specific JIRA project.

    Args:
        Resource (type): The base class for implementing Flask-RESTful
        resources.

    Attributes:
        jira_project (str): The name or identifier of the project associated with
        the tasks.
    """

    def get(self, jira_project=None, jira_component=None, jira_fields=None):
        """
        Retrieves tasks associated with a specific project from JIRA.

        Args:
            jira_project (str, optional): The name or identifier of the project. If
            not provided, retrieves tasks for all projects. Example: LAVA
            jira_component (str): Example: CDH-Premier-Respiratory
            jira_fields (str):  Default to None

        Returns:
            dict: A dictionary containing the retrieved tasks.

        Note:
            This method communicates with JIRA to fetch the tasks.

        Example: LAVA

        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span(f"tasks/{jira_project}"):
            try:
                config = app.cdc_config
                cdh_databricks_kv_scope = config.get("cdh_databricks_kv_scope")
                az_kv_key_vault_name = config.get("az_kv_key_vault_name")
                data_product_id = "lava_core"
                environment = "dev"
                client_secret = config.get("client_secret")
                tenant_id = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_client_id")
                az_kv_key_vault_name = config.get("az_kv_key_vault_name")
                running_interactive = False
                if not client_secret:
                    running_interactive = True

                az_sub_web_client_secret_key = config.get(
                    "az_sub_web_client_secret_key"
                )
                obj_az_keyvault = cdh_az_key_vault.AzKeyVault(
                    tenant_id,
                    client_id,
                    client_secret,
                    az_kv_key_vault_name,
                    running_interactive,
                    data_product_id,
                    environment,
                    az_sub_web_client_secret_key,
                )

                jira_client_secret_key = config.get("jira_client_secret_key")
                jira_client_secret = obj_az_keyvault.get_secret(
                    jira_client_secret_key, cdh_databricks_kv_scope
                )
                if jira_client_secret is None:
                    raise Exception(
                        f"Unable to get Jira client secret from key_vault {jira_client_secret_key}"
                    )
                else:
                    logger.info(f"jira_client_secret_length:{len(jira_client_secret)}")
                    logger.info(
                        f"jira_client_secret_length:{str(len(jira_client_secret))}"
                    )

                if jira_project is None:
                    jira_project = "LAVA"  # Set your default jira_project value here

                jira_base_url = config.get("jira_base_url")
                jira_base_url = jira_base_url.rstrip("/")

                headers = {
                    "Authorization": f"Basic {jira_client_secret}",
                    "Content-Type": "application/json",
                }
                logger.info(f"headers:{headers}")
                logger.info(f"Retrieving tasks for project {jira_project}")

                jira_client_instance = jira_client.JiraClient()
                jira_tasks = jira_client_instance.get_tasks(
                    jira_project,
                    headers,
                    jira_base_url,
                    jira_component,
                    jira_fields,
                    data_product_id,
                    environment,
                )

                logger.info(jira_tasks)
                return jira_tasks

            except Exception as ex:
                msg = f"An unexpected error occurred: {str(ex)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
                ).force_flush()
                return {"error": f"An unexpected error occurred: {msg}"}

 
ns_jira.add_resource(
    Task,
    "/task/<string:jira_project>/<string:jira_component>/', defaults={'jira_fields': None}",
)
ns_jira.add_resource(
    Issue, "/issue/<string:jira_project>/<string:jira_issue_id>/<string:jira_fields>"
)
ns_jira.add_resource(
    Issue,
    "/issue/<string:jira_project>/<string:jira_issue_id>/",
    defaults={"jira_fields": None},
)

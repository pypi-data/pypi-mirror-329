import os
import sys
import requests
from typing import List
import json

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

from cdh_lava_core.cdc_tech_environment_service import environment_file as cdc_env_file
from cdh_lava_core.cdc_tech_environment_service.environment_http import EnvironmentHttp

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

TIMEOUT_5_SEC = 5
TIMEOUT_ONE_MIN = 60


class JiraClient:
    @classmethod
    def get_tasks(
        cls, jira_project, jira_headers, jira_base_url, jira_component, jira_fields, data_product_id, environment
    ):
        """
        Retrieves the tasks for a specific Jira project.

        This method sends a GET request to the Jira API and fetches all tasks associated with the provided project. The method returns a dictionary containing all tasks in the "issues" field of the response. In case of an unsuccessful request, it raises an exception.

        Parameters:
        - jira_project: A string representing the Jira project for which to fetch tasks.
        - jira_headers: A dictionary containing the request headers for the Jira API request.
        - jira_base_url: A string representing the base URL of the Jira API.
        - jira_component: Component to filter
        - jira_fields: Fields to select

        Returns:
        - A dictionary containing all tasks associated with the provided Jira project.

        Raises:
        - requests.exceptions.RequestException: If the GET request to the Jira API fails.
        - Exception: If there's a problem parsing the API response or if the response indicates a server error.
        """

        try:
            tracer, logger = LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
            ).initialize_logging_and_tracing()

            with tracer.start_as_current_span("get_tasks"):
                try:
                    logger_singleton = LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    )
                    jira_base_url = jira_base_url.rstrip("/")
                    api_path = "/rest/api/latest/search"
                    api_url = f"{jira_base_url}{api_path}"

                    if jira_fields is None or jira_fields == "":
                        jira_fields = f"component , issuetype, id,link,name,abbreviation,assigned,is_blocked_by,due_date,status,summary, description"
                        jira_fields = jira_fields.replace(" ", "")
                        
                    fields =   jira_fields.split(',')

                    params = {
                        "jql": f"project = {jira_project} AND component = \"{jira_component}\"",
                        "fields": fields,
                    }

                    obj_env_http = EnvironmentHttp()

                    all_tasks = []
                    start_at = 0
                    max_results = 50  # Or another value up to 100, based on Jira's limits
                    is_last = False
 
                    while not is_last:
                        
                        response_jira_tasks = obj_env_http.get(
                            api_url,
                            jira_headers,
                            TIMEOUT_5_SEC,
                            params,
                            data_product_id,
                            environment,
                        )

                        msg = f"Retrieving tasks for jira_project {jira_project}"
                        logger.info(msg)
                        logger.info(f"api_url: {api_url}")
                        logger.info(f"params: {params}")
                        response_jira_tasks_status_code = response_jira_tasks.status_code
                        msg = "response_jira_tasks_status_code:"
                        msg = msg + f"{response_jira_tasks_status_code}"
                        logger.info(msg)
                        content_t = response_jira_tasks.content.decode("utf-8")
                        response_jira_tasks_content = content_t
                        error_message = msg
                        if response_jira_tasks_status_code in (200, 201):
                            msg = "response_jira_tasks_content:"
                            msg = msg + f"{response_jira_tasks_content}"
                            logger.info(msg)
                            try:
                                data = response_jira_tasks.json()
                                issues = data.get('issues', [])
                                all_tasks.extend(issues)
        
                                logger_singleton.force_flush()
                                # Check if we have fetched all issues
                                is_last = start_at + len(issues) >= data['total']
                                start_at += max_results        # Check if we have fetched all issues
                                is_last = start_at + len(issues) >= data['total']
                                start_at += max_results
                            except ValueError:
                                msg = f"Failed to retrieve json tasks from url: {api_url}."
                                msg = msg + f" parms:{params}"
                                msg = msg + "response_jira_tasks_content:"
                                msg = msg + f"{response_jira_tasks_content}"
                                exc_info = sys.exc_info()
                                logger_singleton.error_with_exception(msg, exc_info)
                                logger_singleton.force_flush()
                                raise
                        else:
                            msg = f"Failed to retrieve tasks from url:{api_url}"
                            msg = msg + f": status_code: {response_jira_tasks.status_code}"
                            msg = msg + ": response_jira_tasks_content:"
                            msg = msg + f"{response_jira_tasks_content}"
                            if response_jira_tasks.status_code == 500:
                                try:
                                    error_message = response_jira_tasks.json()["message"]
                                except ValueError:
                                    error_message = "Failed to retrieve json from url:"
                                    error_message = (
                                        error_message + f"{api_url}: params: {params}."
                                    )
                            msg = msg + ": error_message: " + error_message
                            raise Exception(ValueError, msg)
                        
                        return all_tasks
                except requests.exceptions.RequestException as ex_r:
                    error_msg = "Error in requests: %s", str(ex_r)
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise
                except Exception as ex_:
                    error_msg = "Error: %s", str(ex_)
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise

        except Exception as ex:
            msg = f"An unexpected error occurred: {str(ex)}"
            exc_info = sys.exc_info()
            logger_singleton.error_with_exception(msg, exc_info)
            raise


    @classmethod
    def get_issue(
        cls, jira_project, jira_headers, jira_base_url, jira_issue_id, jira_fields, data_product_id, environment
    ):
        """
        Retrieves the tasks for a specific Jira project.

        This method sends a GET request to the Jira API and fetches all tasks associated with the provided project. The method returns a dictionary containing all tasks in the "issues" field of the response. In case of an unsuccessful request, it raises an exception.

        Parameters:
        - jira_project: A string representing the Jira project for which to fetch tasks.
        - jira_headers: A dictionary containing the request headers for the Jira API request.
        - jira_base_url: A string representing the base URL of the Jira API.
        - jira_issue_id: A string representing the issue key in Jira API.
        - jira_fields: A string with list of columns to return from JIRA
        
        Returns:
        - A dictionary containing the select issue associated with the provided Jira project.

        Raises:
        - requests.exceptions.RequestException: If the GET request to the Jira API fails.
        - Exception: If there's a problem parsing the API response or if the response indicates a server error.
        """

        try:
            tracer, logger = LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
            ).initialize_logging_and_tracing()

            with tracer.start_as_current_span("get_task"):
                try:
                    logger_singleton = LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    )
                    if jira_fields is None or jira_fields == "":
                        jira_fields = f"component , issuetype, id,link,name,abbreviation,assigned,is_blocked_by,due_date,status,summary, description"
                        jira_fields = jira_fields.replace(" ", "")
                        
                    jira_base_url = jira_base_url.rstrip("/")
                    api_path = f"/rest/api/latest/issue/{jira_issue_id}?fields={jira_fields}"
                    api_url = f"{jira_base_url}{api_path}"
 
                    params = {}

                    obj_env_http = EnvironmentHttp()

                    response_jira_task = obj_env_http.get(
                        api_url,
                        jira_headers,
                        TIMEOUT_5_SEC,
                        params,
                        data_product_id,
                        environment,
                    )

                    msg = f"Retrieving tasks for jira_project {jira_project}"
                    logger.info(msg)
                    logger.info(f"api_url: {api_url}")
                    logger.info(f"params: {params}")
                    response_jira_task_json = response_jira_task.json()
                    response_jira_tasks_status_code = response_jira_task.status_code
                    msg = "response_jira_tasks_status_code:"
                    msg = msg + f"{response_jira_tasks_status_code}"
                    logger.info(msg)
                    content_t = response_jira_task.content.decode("utf-8")
                    response_jira_tasks_content = content_t
                    error_message = msg
                    if response_jira_tasks_status_code in (200, 201):
                        msg = "response_jira_tasks_content:"
                        msg = msg + f"{response_jira_tasks_content}"
                        logger.info(msg)
                        try:
                            logger.info(f"issue: {response_jira_task_json}")
                            # Process the retrieved tasks as needed
                            logger_singleton.force_flush()
                            return response_jira_task_json
                        except ValueError:
                            msg = f"Failed to retrieve json tasks from url: {api_url}."
                            msg = msg + f" parms:{params}"
                            msg = msg + "response_jira_tasks_content:"
                            msg = msg + f"{response_jira_tasks_content}"
                            exc_info = sys.exc_info()
                            logger_singleton.error_with_exception(msg, exc_info)
                            logger_singleton.force_flush()
                            raise
                    else:
                        msg = f"Failed to retrieve tasks from url:{api_url}"
                        msg = msg + f": status_code: {response_jira_task.status_code}"
                        msg = msg + ": response_jira_tasks_content:"
                        msg = msg + f"{response_jira_tasks_content}"
                        if response_jira_task.status_code == 500:
                            try:
                                error_message = response_jira_task.json()["message"]
                            except ValueError:
                                error_message = "Failed to retrieve json from url:"
                                error_message = (
                                    error_message + f"{api_url}: params: {params}."
                                )
                        msg = msg + ": error_message: " + error_message
                        raise Exception(ValueError, msg)
                except requests.exceptions.RequestException as ex_r:
                    error_msg = "Error in requests: %s", str(ex_r)
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise
                except Exception as ex_:
                    error_msg = "Error: %s", str(ex_)
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise

        except Exception as ex:
            msg = f"An unexpected error occurred: {str(ex)}"
            exc_info = sys.exc_info()
            logger_singleton.error_with_exception(msg, exc_info)
            raise

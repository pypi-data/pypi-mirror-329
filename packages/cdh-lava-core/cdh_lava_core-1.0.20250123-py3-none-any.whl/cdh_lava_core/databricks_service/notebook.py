"""
This module contains the implementation of a Databricks notebook class and related functions.

The module includes the following classes:
- Notebook: A class representing a Databricks notebook.

The module includes the following functions:
- fix_file_path_if_windows: Fixes the file path for Windows OS by normalizing backslashes and forward slashes.
- run_notebook: Run a Databricks notebook using the Databricks REST API.
"""

import sys
import os
import time
import requests
import datetime

from requests.exceptions import HTTPError

OS_NAME = os.name
sys.path.append("../..")

if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_tech_environment_service.environment_http import EnvironmentHttp

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class Notebook:
    """
    A class representing a Databricks notebook.

    Methods:
    - run_notebook: Run a Databricks notebook using the Databricks REST API.
    """

    @staticmethod
    def fix_file_path_if_windows(path):
        """
        Fixes the file path for Windows OS by normalizing backslashes and forward slashes.

        Args:
        path (str): The file path to be fixed.

        Returns:
        str: The normalized file path for Windows, or the original path for other OS.
        """
        # Check if the operating system is Windows
        if os.name == "nt":
            # Normalize the path by replacing backslashes with forward slashes
            normalized_path = path.replace("\\", "/")

            # Further normalize using os.path.normpath to handle any other irregularities
            return os.path.normpath(normalized_path)
        else:
            # If not Windows, return the original path
            return path

    @classmethod
    def run_notebook_and_poll_status(cls, token, databricks_instance_id, cluster_id, notebook_path, parameters, timeout_minutes: int, data_product_id, environment):
        """
        Submits a notebook run to Databricks and polls for its status until completion.

        Parameters:
        - token (str): Databricks personal access token.
        - databricks_instance_id (str): URL of the Databricks instance.
        - cluster_id (str): ID of the Databricks cluster where the notebook will run.
        - notebook_path (str): Path to the notebook in the Databricks workspace.
        - parameters (dict): Parameters to pass to the notebook.
        - timeout_minutes (int): Maximum duration in minutes to poll before timing out.

        Returns:
        - Final status of the notebook run.
        """
 
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_notebook_and_poll_status"):
            
 
            try:
                                            
                # API URLs
                base_url = f"https://{databricks_instance_id}"
                get_run_url = f"{base_url}/api/2.0/jobs/runs/get"

                # Headers for authentication
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }

                status_object = cls.run_notebook(token, databricks_instance_id, cluster_id, notebook_path, parameters, data_product_id, environment)
                
                run_id = status_object["run_id"]
                # Initialize timeout control
                start_time = datetime.datetime.now()
                timeout = datetime.timedelta(minutes=timeout_minutes)


                # Polling for status
                while True:
                    current_time = datetime.datetime.now()
                    if current_time - start_time > timeout:
                        logger.error("Timeout reached, terminating the status check.")
                        raise TimeoutError("Notebook run polling timed out.")

                    time.sleep(30)  # Poll every 30 seconds
                    status_response = requests.get(f"{get_run_url}?run_id={run_id}", headers=headers)
                    status_response.raise_for_status()
                    run_info = status_response.json()

                    state = run_info['state']
                    life_cycle_state = state['life_cycle_state']
                    logger.info(f"life_cycle_state: str(life_cycle_state)")
                    # Check the status of the notebook run
                  # Check the status of the notebook run
                    if life_cycle_state in ['SKIPPED', 'INTERNAL_ERROR']:
                        result_state = state.get('result_state', 'No result due to error or skipping.')
                        error_message = state.get('state_message', 'No detailed error message provided.')
                                    
                        logger.error(f"Notebook run completed. Final state: {life_cycle_state}. "
                                    f"Result state: {result_state}. Error message: {error_message}")
                        return run_info
                    elif life_cycle_state in ['TERMINATED']:
                        result_state = state.get('result_state', 'No result due to error or skipping.')
                        error_message = state.get('state_message', 'No detailed error message provided.')
                                    
                        logger.warning(f"Notebook run completed. Final state: {life_cycle_state}. "
                                    f"Result state: {result_state}. Error message: {error_message}")
                        return run_info
                    else:
                        logger.info(f"Notebook run is in progress. Current state: {life_cycle_state}.")
                 
            except Exception as e:
                    logger.error(f"An exception occurred: {e}")
                    raise e

    @classmethod
    def run_notebook(
        cls,
        token,
        databricks_instance_id,
        cdh_databricks_cluster,
        notebook_path,
        parameters,
        data_product_id,
        environment,
    ):
        """
        Run a Databricks notebook using the Databricks REST API.

        Parameters:
        - dbx_pat_token (str): Databricks personal access token.
        - databricks_instance_id (str): URL of the Databricks instance.
        - cdh_databricks_cluster (str): ID of the Databricks cluster to run the notebook.
        - notebook_path (str): Path to the notebook in the Databricks workspace.
        - parameters (dict): Dictionary of notebook parameters.

        Returns:
        - response (dict): The JSON response from the Databricks API.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_notebook"):
            try:
                bearer = "Bearer " + token
                api_url = f"https://{databricks_instance_id}/api/2.0/jobs/runs/submit"
                logger.info(f"Attempting run_notebook for notebook_path: {notebook_path}")

                headers = {
                    "Authorization": bearer,
                    "Content-Type": "application/json",
                }

                payload = {
                    "run_name": "Databricks Notebook Run",
                    "existing_cluster_id": cdh_databricks_cluster,
                    "notebook_task": {
                        "notebook_path": notebook_path,
                        "base_parameters": parameters,
                    },
                }

                status_object = {"status": "initiated", "data": None, "error": None, "run_id": None}

                obj_http = EnvironmentHttp()
                response = obj_http.post(api_url, headers, 120, data_product_id, environment, json=payload)

                if response.status_code == 200:
                    logger.info("Notebook run successfully initiated.")
                    status_object["status"] = "success"
                    status_object["data"] = response.json()
                    status_object["run_id"] = response.json()['run_id']
                else:
                    response.raise_for_status()

                return status_object
            except HTTPError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")
                status_object["status"] = "error"
                status_object["error"] = str(http_err)
                raise
            except Exception as ex:
                logger.error(f"An error occurred: {ex}")
                status_object["status"] = "error"
                status_object["error"] = str(ex)
                raise

    
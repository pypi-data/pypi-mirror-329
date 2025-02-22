from azure.storage.queue import QueueServiceClient
from azure.identity import ClientSecretCredential
import requests
import os
import cdh_lava_core.cdc_tech_environment_service.environment_http as cdc_env_http

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

from cdh_lava_core.cdc_tech_environment_service import environment_file as cdc_env_file
import pathlib
from cdh_lava_core.az_storage_service import  az_storage_file

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
from pathlib import Path

import subprocess

class GitHubRepo:
    """
    Represents a GitHub gh_repo_name and provides methods to download its contents.
    """

    @staticmethod
    def clone_repo(gh_owner_name, gh_repo_name, gh_branch_name, destination_folder, data_product_id, environment):
        """
        Clone a Git repository into the specified destination folder.

        Args:
            git_url (str): The URL of the Git repository to clone.
            destination_folder (str): The path to the folder where the repository will be cloned.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the cloning is performed.

        Returns:
            bool: True if the repository was cloned successfully, False otherwise.

        Raises:
            ValueError: If the repository cloning fails.

        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("clone_repo"):
            try:
                git_url = f'https://github.com/{gh_owner_name}/{gh_repo_name}.git'
                    
                # Ensure the destination folder exists
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)


                repo_dir = os.path.join(destination_folder, gh_repo_name)
                
                # Clone the repository
                try:
                    result = subprocess.run(['git', 'clone', git_url, repo_dir],
                                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        logger.error(f"Failed to clone repository: {result.stderr}")
                        raise ValueError(f"Failed to clone repository: {result.stderr}")
                    else:
                        logger.info("Repository cloned successfully.")
                except Exception as e:
                    logger.error(f"Exception during cloning: {str(e)}")
                    raise ValueError(f"Exception during cloning: {str(e)}")


                # Change into the cloned repository directory and checkout the branch
                try:
                    # Checkout the specific branch
                    result = subprocess.run(['git', 'checkout', gh_branch_name],
                                            cwd=repo_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        logger.error(f"Failed to checkout branch {gh_branch_name}: {result.stderr}")
                        raise ValueError(f"Failed to checkout branch {gh_branch_name}: {result.stderr}")
                    else:
                        logger.info(f"Checked out branch: {gh_branch_name}")

                except Exception as e:
                    logger.error(f"Exception during branch checkout: {str(e)}")
                    raise ValueError(f"Exception during branch checkout: {str(e)}")

                logger.info(f"Repository cloned successfully into {destination_folder}")
                return "Success"
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone repository: {e}")
                raise ValueError(f"Failed to clone repository: {e}")


    @staticmethod
    def clone_private_repo(gh_access_token, gh_owner_name, gh_repo_name, gh_branch_name, destination_folder, data_product_id, environment):
        """
        Clone a Git repository into the specified destination folder.

        Args:
            git_url (str): The URL of the Git repository to clone.
            destination_folder (str): The path to the folder where the repository will be cloned.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the cloning is performed.

        Returns:
            bool: True if the repository was cloned successfully, False otherwise.

        Raises:
            ValueError: If the repository cloning fails.

        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("clone_repo"):
            try:
                if gh_access_token is not None:
                    git_url = f'https://{gh_access_token}:x-oauth-basic@github.com/{gh_owner_name}/{gh_repo_name}.git'
                else:
                    git_url = f'https://github.com/{gh_owner_name}/{gh_repo_name}.git'
                    
                # Ensure the destination folder exists
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                # Execute the git clone command
                try:
                    subprocess.check_call(['git', 'clone', git_url, destination_folder], cwd=destination_folder)
                    logger.info("Repository cloned successfully.")
                except subprocess.CalledProcessError as e:
                    logger.info(f"Failed to clone repository: {e}")

                repo_dir = os.path.join(destination_folder, gh_repo_name)

                # Change into the cloned repository directory
                try:
                    subprocess.check_call(['cd', repo_dir], shell=True)
                    logger.info(f"Changed to repository directory: {gh_repo_name}")
                except subprocess.CalledProcessError as e:
                    logger.info(f"Failed to change directory: {e}")

                # Checkout the specific branch
                try:
                    subprocess.check_call(['git', 'checkout', gh_branch_name], cwd=repo_dir)
                    logger.info(f"Checked out branch: {gh_branch_name}")
                except subprocess.CalledProcessError as e:
                    logger.info(f"Failed to checkout branch: {e}")


                logger.info(f"Repository cloned successfully into {destination_folder}")
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone repository: {e}")
                raise ValueError(f"Failed to clone repository: {e}")


    @staticmethod
    def download_repo(config, gh_access_token, gh_owner_name, gh_repo_name, gh_branch_name, dest_file_path, data_product_id, environment):
        """
        Downloads the contents of a GitHub gh_repo_name.

        Args:
            config (object): The configuration object.
            gh_access_token (str): The GitHub access token.
            gh_owner_name (str): The gh_owner_name of the gh_repo_name.
            gh_repo_name (str): The name of the gh_repo_name.
            gh_branch_name (str): The gh_branch_name of the gh_repo_name.
            dest_file_path (str): The destination file path.
            data_product_id (str): The ID of the data product.
            environment (str): The environment.

        Raises:
            ValueError: If the gh_repo_name contents could not be retrieved.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        HTTP_TIMEOUT = 30
        
        with tracer.start_as_current_span("download_repo"):
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {gh_access_token}",
            }
                
            api_url = f"https://api.github.com/repos/{gh_owner_name}/{gh_repo_name}/git/trees/{gh_branch_name}?recursive=1"
            obj_http = cdc_env_http.EnvironmentHttp()
            response = obj_http.get(api_url, headers, HTTP_TIMEOUT, None, data_product_id, environment  )
            response_json = response.json()
            file_counter = 0
            if 'tree' in response_json:
                for file in response_json['tree']:
                    if file['type'] == 'blob':  # Only download blobs (files)
                        file_counter += 1
                        print(f"Downloading {file['path']}...")
                        file_path = file['path']
                        dest_file_name = os.path.basename(file_path)
                        src_url = f"https://raw.githubusercontent.com/{gh_owner_name}/{gh_repo_name}/{gh_branch_name}/{file_path}"
                        logger.info(f"File: {file['path']}, Raw src_url: {src_url}")
                        
                        obj_environment_file = az_storage_file.AzStorageFile()
                        
                        file_path_os = Path(file_path)
                        directory_path = file_path_os.parent

                        dest_path = os.path.join(dest_file_path, directory_path, dest_file_name)

                        dest_path = obj_environment_file.convert_abfss_to_https_path(
                            dest_path, data_product_id, environment
                        )
                        logger.info(f"dest_path:{dest_path}")

                        logger.info(f"src_url:{src_url}")
                        result_message = obj_environment_file.copy_url_to_blob(
                            config,
                            src_url,
                            dest_path,
                            dest_file_name,
                            data_product_id,
                            environment,
                        )
                        
                        logger.info(f"result_message: {result_message}")
                
                if file_counter == 0:
                    logger.error("No files to download.")
                    raise ValueError("No files to download.")
                else:
                    return 200, result_message
                        
            else:
                logger.error("Could not retrieve gh_repo_name contents.")
                raise ValueError("Could not retrieve gh_repo_name contents.")
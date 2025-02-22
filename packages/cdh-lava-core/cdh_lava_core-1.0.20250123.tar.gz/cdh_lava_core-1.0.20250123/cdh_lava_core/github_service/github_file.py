import requests
import base64
import json
import os
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class GitHubFile:

    @staticmethod
    def push_to_github(data_product_id, environment, repo_owner, repo_name, file_path, local_file_path, commit_message, branch="main", access_token=None):
        """
        Push a local file to a GitHub repository, creating or updating the file as necessary.

        Args:
            data_product_id (str): Identifier for the data product.
            environment (str): The environment in which the service is running.
            repo_owner (str): The owner of the GitHub repository.
            repo_name (str): The name of the GitHub repository.
            file_path (str): The path in the repository where the file will be stored.
            local_file_path (str): The local path of the file to be pushed.
            commit_message (str): The commit message for the push.
            branch (str, optional): The branch to which the file will be pushed. Defaults to "main".
            access_token (str, optional): The GitHub access token for authentication. Defaults to None.

        Returns:
            dict: A dictionary containing either a success message or an error message.
        """

        tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("push_to_github"):

            try:
                if not access_token:
                    raise ValueError("GitHub access token is required for authentication.")


                file_path = file_path.lstrip("/")  # Remove leading slash if present
                # GitHub API URL for the contents endpoint
                api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

                headers = {
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/vnd.github+json'
                }

                # Read the contents of the local file to be pushed
                with open(local_file_path, 'r') as file:
                    content = file.read()

                # Encode file content in base64 (required by GitHub API)
                content_encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')

                # Get the file's SHA (required for updating existing files)
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    sha = response.json()['sha']  # Get SHA of the existing file
                elif response.status_code == 404:
                    sha = None  # File doesn't exist, so it will be created
                else:
                    return {"error": f"Failed to fetch file metadata: {response.json()}"}

                # Payload for creating/updating the file
                data = {
                    "message": commit_message,
                    "content": content_encoded,
                    "branch": branch,
                }
                if sha:
                    data["sha"] = sha  # Include SHA if updating

                # Make the PUT request to create or update the file
                response = requests.put(api_url, headers=headers, data=json.dumps(data))

                if response.status_code in [200, 201]:
                    return {"message": f"File pushed successfully to branch '{branch}'."}
                else:
                    return {"error": f"Failed to push to GitHub: {response.json()}"}

            except Exception as e:
                return {"error": f"An error occurred: {str(e)}"}

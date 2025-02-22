# Example usage
# http_util = EnvironmentHttp()
# url = 'https://example.com/api/data'
# try:
#    response = http_util.get(url)
#    print(response.text)
# except Exception as e:
#    print(f"Error occurred: {str(e)}")

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton


import requests
from retrying import retry
import os
import sys
from urllib.parse import urlencode
from subprocess import CompletedProcess
from collections import namedtuple
import json
import subprocess

# Define a simple response class to mimic the structure of requests.Response
Response = namedtuple("Response", ["status_code", "text"])

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class HTTPError(Exception):
    """Custom HTTPError for handling HTTP error responses and subprocess exceptions."""

    def __init__(self, message, returncode=None, text=None):
        self.message = message
        self.returncode = returncode
        self.text = text
        super().__init__(message)


class DetailedResponse:
    def __init__(self, completed_process: CompletedProcess):
        self.completed_process = completed_process
        self.status_code = self._extract_status_code()
        self.text = completed_process.stdout

    def json(self):
        """Attempt to parse the stdout as JSON. Returns the parsed JSON if possible."""
        try:
            return json.loads(self.text)
        except json.JSONDecodeError as e:
            raise ValueError("Failed to decode JSON") from e

    def raise_for_status(self):
        """Raise HTTPError if the command failed, indicated by a non-zero returncode."""
        if self.completed_process.returncode != 0:
            raise HTTPError(
                "Command execution failed",
                returncode=self.completed_process.returncode,
                text=self.text,
            )

    def _extract_status_code(self):
        """A placeholder method to extract the HTTP status code from the subprocess output.

        This is highly dependent on your specific use case and how the subprocess output is formatted.
        You might need to parse the `self.text` attribute to find the HTTP status code if it's included in the output.
        For simplicity, this example will just return 200 if the command succeeded, or 400 otherwise.
        """
        return 200 if self.completed_process.returncode == 0 else 400


class EnvironmentHttp:
    """
    Utility class for making HTTP requests with retry functionality.
    """

    def __init__(self):
        pass

    def create_curl(self, url, headers=None, timeout=10, params=None):
        """
        Generates a cURL command for GET requests, including headers and URL-encoded parameters.
        """
        # Initialize the curl command list
        curl_command_parts = ["curl", "-X", "GET"]

        # Safely quote the URL
        curl_command_parts.append(f"'{url}'")

        # Include headers, ensuring they are properly quoted
        headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        for header, value in headers.items():
            curl_command_parts.append(f"-H '{header}: {value}'")

        # Set the timeout
        curl_command_parts.append(f"-m {timeout}")

        # Append URL-encoded parameters if provided
        if params:
            for param, value in params.items():
                curl_command_parts.append(f"--data-urlencode '{param}={value}'")

        return " ".join(curl_command_parts)

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_curl(
        self,
        url,
        headers=None,
        timeout=30,
        params=None,
        data_product_id=None,
        environment=None,
    ):
        """
        Make a GET request to the specified URL with retry functionality.
        Now simplified to focus on actual GET behavior.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_curl"):
            try:

                # Example usage, assuming `result` is the output of subprocess.run() for your cURL command:
                curl_command = self.create_curl(url, headers, timeout, params)
                result = subprocess.run(
                    curl_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                response = DetailedResponse(result)

                response.raise_for_status()
                data = response.json()
                logger.info(data)  # Use the JSON data as needed
                return response
            except HTTPError as e:
                logger.error(f"Request failed: {e.message}")
                raise e
            except ValueError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                raise e
            except Exception as err:
                error_msg = f"Error {err} occurred while making GET request to {url}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                curl_command = self.create_curl(url, headers, timeout, params)
                logger.error("curl of failed request: " + curl_command)
                raise err

    # Retry on 403 errors wait 5 seconds between retries
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get(
        self,
        url,
        headers,
        timeout,
        params,
        data_product_id,
        environment,
        encode_params=False,
    ):
        """
        Make a GET request to the specified URL with retry functionality for 403 errors.

        Args:
            url (str): The URL to make the GET request to.
            headers (dict, optional): Dictionary of HTTP headers to send with the request. Defaults to None.
            timeout (float or tuple, optional): Timeout value for the request in seconds. Defaults to None.
            params (dict, optional): Dictionary of query parameters to include in the request. Defaults to None.

        Returns:
            requests.Response: The response object.

        Raises:
            requests.exceptions.HTTPError: If a non-403 HTTP error occurs.
            Exception: If a 403 error occurs after retrying.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        # Counter variable to track the number of 403 errors
        error_count = 0

        with tracer.start_as_current_span("get"):
            try:
                url = self.fix_url_slashes(url)

                if params is None and len(headers) > 0:
                    response = requests.get(
                        url, headers=headers, timeout=timeout, verify=True
                    )
                elif params is None and len(headers) == 0:
                    response = requests.get(url, timeout=timeout, verify=True)
                elif params is not None and len(headers) > 0 and encode_params is False:
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=timeout,
                        params=params,
                        verify=True,
                    )
                elif (
                    params is not None and len(headers) == 0 and encode_params is False
                ):
                    response = requests.get(
                        url,
                        timeout=timeout,
                        params=params,
                        verify=True,
                    )
                elif params is not None and len(headers) > 0 and encode_params is True:
                    encoded_params = urlencode(params)
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=timeout,
                        params=encoded_params,
                        verify=True,
                    )
                elif params is not None and len(headers) == 0 and encode_params is True:
                    encoded_params = urlencode(params)
                    response = requests.get(
                        url,
                        timeout=timeout,
                        params=encoded_params,
                        verify=True,
                    )

                if response.status_code == 403:
                    error_count += 1
                    if error_count <= 2:
                        error_msg = f"Warning: 403 Error occurred while making GET request to {url}"
                        logger.warning(error_msg)
                        curl_command = self.create_curl(url, headers, timeout, params)
                        logger.warning("curl of failed request: " + curl_command)
                    else:
                        error_msg = f"Error: 403 Error occurred while making GET request to {url}"
                        logger.error(error_msg)
                        curl_command = self.create_curl(url, headers, timeout, params)
                        logger.error("curl of failed request: " + curl_command)
                    response.raise_for_status()

                    logger.info("response_length: " + str(len(response.text)))
                return response

            except Exception as err:
                error_msg = f"Error {err} occurred while making GET request to {url}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                curl_command = self.create_curl(url, headers, timeout, params)
                logger.error("curl of failed request: " + curl_command)
                raise err

    # Retry on 403 errors wait 5 seconds between retries
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def post(self, url, headers, timeout, data_product_id, environment, json=None):
        """
        Sends a POST request to the specified URL with the given headers, timeout, data product ID, environment, and optional JSON payload.

        Args:
            url (str): The URL to send the POST request to.
            headers (dict): The headers to include in the request.
            timeout (float): The maximum number of seconds to wait for the request to complete.
            data_product_id (str): The ID of the data product.
            environment (str): The environment to use for the request.
            json (dict, optional): The JSON payload to include in the request.

        Returns:
            requests.Response: The response object returned by the server.

        Raises:
            requests.exceptions.HTTPError: If a 403 error occurs during the request.
            Exception: If any other error occurs during the request.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        # Counter variable to track the number of 403 errors
        error_count = 0

        with tracer.start_as_current_span("post"):
            try:
                url = self.fix_url_slashes(url)

                if json is None:
                    response = requests.post(
                        url, headers=headers, timeout=timeout, verify=True
                    )
                else:
                    response = requests.post(
                        url, headers=headers, timeout=timeout, json=json, verify=True
                    )

                if response.status_code == 403:
                    error_count += 1
                    if error_count <= 2:
                        error_msg = f"Warning: 403 Error occurred while making GET request to {url}"
                        logger.warning(error_msg)
                        curl_command = self.create_curl(url, headers, timeout, json)
                        logger.warning("curl of failed request: " + curl_command)
                    else:
                        error_msg = f"Error: 403 Error occurred while making GET request to {url}"
                        logger.error(error_msg)
                        curl_command = self.create_curl(url, headers, timeout, json)
                        logger.error("curl of failed request: " + curl_command)
                    response.raise_for_status()
                return response

            except Exception as err:
                error_msg = f"Error {err} occurred while making GET request to {url}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                curl_command = self.create_curl(url, headers, timeout, json)
                logger.error("curl of failed request: " + curl_command)
                raise err

    def fix_url_slashes(self, url):
        """
        Fixes the slashes in a URL string by ensuring that all slashes are forward slashes, except for
        the protocol part (e.g., http:// or https://).

        Args:
        url (str): The URL with potentially incorrect slashes.

        Returns:
        str: The URL with corrected slashes.
        """
        # Split the URL into protocol and the rest
        parts = url.split("://")
        if len(parts) == 2:
            protocol, rest = parts
            # Replace backslashes with forward slashes in the rest of the URL
            fixed_rest = rest.replace("\\", "/")
            # Reconstruct the URL
            return f"{protocol}://{fixed_rest}"
        else:
            # If the URL doesn't have a protocol, just replace backslashes
            return url.replace("\\", "/")

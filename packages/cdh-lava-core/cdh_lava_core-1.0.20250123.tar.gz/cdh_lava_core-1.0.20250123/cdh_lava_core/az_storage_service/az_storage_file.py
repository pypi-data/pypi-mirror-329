from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import HttpResponseError
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeDirectoryClient
from urllib.parse import urlparse
from cdh_lava_core.databricks_service import repo_core as databricks_repo_core
import os
from urllib.parse import urlparse
import logging
# error handling
from subprocess import check_output, Popen, PIPE, CalledProcessError
import os
import sys
import subprocess
import requests

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_tech_environment_service.environment_http import EnvironmentHttp


class AzStorageFile:
    """
    A class that provides utility methods for working with files in Azure Data Lake Storage.
    """

    @staticmethod
    def get_file_size(
        account_url: str,
        tenant_id,
        client_id: str,
        client_secret: str,
        storage_container: str,
        file_path: str,
        data_product_id: str,
        environment: str,
    ):
        """
        Retrieves the size of a file in an Azure Data Lake Storage account.

        Args:
            account_url (str): The URL of the Azure Storage account. Example: https://<account_name>.dfs.core.windows.net.
            tenant_id (str): The tenant ID of the Azure Active Directory.
            client_id (str): The client ID of the Azure Active Directory application.
            client_secret (str): The client secret of the Azure Active Directory application.
            storage_container (str): The name of the file system in the Azure Data Lake Storage account.
            file_path (str): The path to the file in the file system.

        Returns:
            int: The size of the file in bytes.

        Raises:
            Exception: If there is an error retrieving the file properties.
        """

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        service_client = DataLakeServiceClient(
            account_url=account_url,
            credential=credential,
        )
        file_system_client = service_client.get_file_system_client(storage_container)
        file_client = file_system_client.get_file_client(file_path)

        try:
            file_props = file_client.get_file_properties()
            return file_props.size  # Returns the size of the file in bytes
        except Exception as e:
            print(e)
            return None

    @classmethod
    def rename_directory(cls, config: dict, source_path, new_directory_name) -> str:
        """
        Renames a directory in Azure Blob File System Storage (ABFSS).

        Args:
            config (dict): The configuration dictionary containing the necessary Azure parameters.
            source_path (str): The original path of the directory to be renamed in ABFSS.
            new_directory_name (str): The new name for the directory.

        Returns:
            str: A message indicating the status of the rename operation.
        """

        try:
            client_id = config["az_sub_client_id"]
            client_secret = config["client_secret"]

            result = "file_adls_copy failed"

            if client_secret is None:
                az_sub_client_secret_key = str(config["az_sub_client_secret_key"])
                key = az_sub_client_secret_key
                client_secret = f"Environment variable: {key} not found"

            os.environ["AZCOPY_SPA_CLIENT_SECRET"] = client_secret
            tenant_id = config["az_sub_tenant_id"]

            running_local = config["running_local"]
            print(f"running_local:{running_local}")
            print(f"source_path:{source_path}")
            print(f"new_directory_name:{new_directory_name}")

            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            storage_account_loc = urlparse(source_path).netloc
            storage_path = urlparse(source_path).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            account_url = f"https://{storage_account_loc}"

            service_client = DataLakeServiceClient(
                account_url=account_url, credential=credential
            )
            file_system_client = service_client.get_file_system_client(
                storage_container
            )

            dir_path = storage_path.replace(f"{storage_container}" + "/", "")

            is_directory = None
            directory_client: DataLakeDirectoryClient
            try:
                directory_client = file_system_client.get_directory_client(dir_path)
                if directory_client.exists():
                    is_directory = True
                else:
                    is_directory = True

                if is_directory:
                    directory_client.rename_directory(new_directory_name)
                    result = "Success"
                else:
                    result = f"rename_directory failed: {dir_path} does not exist"
            except Exception as ex:
                directory_client = DataLakeDirectoryClient("empty", "empty", "empty")
                print(ex)
                result = "rename_directory failed"
        except Exception as ex_rename_directory:
            print(ex_rename_directory)
            result = "rename_directory failed"
        result = str(result)
        return result

    @classmethod
    def folder_adls_create(cls, config, dir_path: str, dbutils) -> str:
        """
        Creates a new directory in Azure Data Lake Storage (ADLS).

        Args:
            config (dict): The configuration dictionary containing the necessary Azure parameters.
            dir_path (str): The path of the directory to be created in ADLS.
            dbutils: An instance of Databricks dbutils, used for filesystem operations.

        Returns:
            str: A message indicating the status of the directory creation operation.
        """

        running_local = config["running_local"]
        client_id = config["az_sub_client_id"]
        client_secret = config["client_secret"]

        if client_secret is None:
            az_sub_client_secret_key = str(config["az_sub_client_secret_key"])
            client_secret = (
                f"Environment variable: {az_sub_client_secret_key} not found"
            )

        os.environ["AZCOPY_SPA_CLIENT_SECRET"] = client_secret
        tenant_id = config["az_sub_tenant_id"]

        storage_account_loc = urlparse(dir_path).netloc
        storage_path = urlparse(dir_path).path
        storage_path_list = storage_path.split("/")
        storage_container = storage_path_list[1]
        account_url = f"https://{storage_account_loc}"

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        service_client = DataLakeServiceClient(
            account_url=account_url, credential=credential
        )
        file_system_client = service_client.get_file_system_client(storage_container)

        return "True"
 

    
    @classmethod
    def file_adls_copy(
        cls,
        config,
        source_path: str,
        destination_path: str,
        from_to: str,
        dbutils,
        data_product_id,
        environment
    ) -> str:
        """
        Copies a file from the local filesystem to Azure Data Lake Storage (ADLS), or vice versa.

        Args:
            config (dict): The configuration dictionary containing the necessary Azure and local filesystem parameters.
            source_path (str): The path of the file to be copied.
            destination_path (str): The path where the file will be copied. If 'bytes' is passed, the function will return a byte array instead of performing a copy.
            from_to (str): Indicates the direction of the copy. 'BlobFSLocal' signifies ADLS to local copy, and 'LocalBlobFS' signifies local to ADLS copy.
            dbutils: An instance of Databricks dbutils, used for filesystem operations.

        Returns:
            str: A message indicating the status of the copy operation.
        """


        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("file_adls_copy"):


            try:
                running_local = not (("dbutils" in locals() or "dbutils" in globals()) and dbutils is not None)

                result = "file_adls_copy failed"
                client_id = config["az_sub_client_id"]
                client_secret = config["client_secret"]
                tenant_id = config["az_sub_tenant_id"]

                # Initialize azcopy_installed to False
                azcopy_installed = False

                try:
                    # Capture the output of the azcopy version command
                    result = subprocess.run(
                        ["azcopy", "--version"], 
                        check=True, 
                        capture_output=True, 
                        text=True  # Ensures output is returned as a string
                    )
                    azcopy_installed = True  # Set to True if the command is successful
                    # Access the standard output
                    logger.info(f"azcopy installed. Version: {result.stdout.strip()}")
                except subprocess.CalledProcessError as e:
                    # azcopy command was found but returned a non-zero exit code
                    logger.warning(f"azcopy command failed with exit code {e.returncode}. Fallback to Python SDK.")
                    logger.warning(f"Error output: {e.stderr}")
                    azcopy_installed = False  # Set to False if there is an error with azcopy
                except FileNotFoundError:
                    # azcopy is not installed or not found in the PATH
                    logger.warning("azcopy not found. Fallback to Python SDK.")
                    azcopy_installed = False  # Set to False if azcopy is not found
                    
                if azcopy_installed and running_local:
                    # Use azcopy if available and running locally
                    p_1 = f"--application-id={client_id}"
                    p_2 = f"--tenant-id={tenant_id}"
                    arr_azcopy_command = [
                        "azcopy",
                        "login",
                        "--service-principal",
                        p_1,
                        p_2,
                    ]
                    arr_azcopy_command_string = " ".join(arr_azcopy_command)
                    logger.info(arr_azcopy_command_string)

                    try:
                        subprocess.check_output(arr_azcopy_command)
                        result_1 = f"login --service-principal {p_1} to {p_2} succeeded"
                    except subprocess.CalledProcessError as ex_called_process:
                        result_1 = str(ex_called_process.output)

                    logger.info(result_1)

                    if from_to == "BlobFSLocal":
                        arr_azcopy_command = [
                            "azcopy",
                            "copy",
                            f"{source_path}",
                            f"{destination_path}",
                            f"--from-to={from_to}",
                            "--recursive",
                            "--trusted-microsoft-suffixes=",
                            "--log-level=INFO",
                        ]
                    elif from_to == "LocalBlobFS":
                        arr_azcopy_command = [
                            "azcopy",
                            "copy",
                            f"{source_path}",
                            f"{destination_path}",
                            "--log-level=DEBUG",
                            f"--from-to={from_to}",
                        ]
                    else:
                        arr_azcopy_command = [f"from to:{from_to} is not supported"]

                    arr_azcopy_command_string = " ".join(arr_azcopy_command)
                    print(arr_azcopy_command_string)

                    try:
                        subprocess.check_output(arr_azcopy_command)
                        result_2 = f"copy from {source_path} to {destination_path} succeeded"
                    except subprocess.CalledProcessError as ex_called_process:
                        result_2 = str(ex_called_process.output)

                    result = result_1 + result_2

                elif not running_local:
                    # Use dbutils when running on Databricks
                    if from_to == "BlobFSLocal":
                        # ADLS to local copy (Databricks -> ADLS)
                        dbutils.fs.cp(source_path, destination_path, recurse=True)
                        result = f"Copied from ADLS {source_path} to Databricks {destination_path}"
                    elif from_to == "LocalBlobFS":
                        # Local to ADLS copy (Databricks -> ADLS)
                        dbutils.fs.cp(source_path, destination_path, recurse=True)
                        result = f"Copied from Databricks {source_path} to ADLS {destination_path}"
                    else:
                        result = f"Unsupported from_to value: {from_to}"
                
                else:
                    # Fallback to Python SDK if azcopy is not installed
                    if from_to == "BlobFSLocal":
                        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
                        storage_account_loc = urlparse(source_path).netloc
                        storage_path = urlparse(source_path).path
                        storage_path_list = storage_path.split("/")
                        storage_container = storage_path_list[1]
                        account_url = f"https://{storage_account_loc}"
                        service_client = DataLakeServiceClient(
                            account_url=account_url, credential=credential
                        )
                        file_system_client = service_client.get_file_system_client(storage_container)
                        dir_path = storage_path.replace(f"{storage_container}/", "")

                        azure_files = file_system_client.get_paths(path=dir_path)
                        for file_path in azure_files:
                            file_client = file_system_client.get_file_client(file_path.name)
                            file_data = file_client.download_file().readall()
                            destination_file_path = os.path.join(destination_path, file_path.name)

                            with open(destination_file_path, "wb") as local_file:
                                local_file.write(file_data)

                            logger.info(f"Copied file to {destination_file_path}")

                        result = f"Copied files from ADLS to {destination_path}."
                    elif from_to == "LocalBlobFS":
                        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
                        storage_account_loc = urlparse(destination_path).netloc
                        storage_path = urlparse(destination_path).path
                        storage_path_list = storage_path.split("/")
                        storage_container = storage_path_list[1]
                        account_url = f"https://{storage_account_loc}"
                        service_client = DataLakeServiceClient(
                            account_url=account_url, credential=credential
                        )
                        file_system_client = service_client.get_file_system_client(storage_container)
                        dir_path = storage_path.replace(f"{storage_container}/", "")
                        dir_path = os.path.dirname(dir_path)
                        # Upload local file to ADLS
                        file_name = os.path.basename(source_path)
                        file_client = file_system_client.get_file_client(os.path.join(dir_path, file_name))

                        with open(source_path, "rb") as local_file:
                            file_client.upload_data(local_file.read(), overwrite=True)

                        logger.info(f"Uploaded file from {source_path} to {destination_path}")

                        result = f"Uploaded file to {destination_path}."
                    else:
                        result = f"Unsupported from_to value: {from_to}"

                return result
            except Exception as ex:
                    logger.error(f"error in test copy from {source_path} if path exists: {destination_path}")                        
                    error_msg = "Error: %s", ex
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise

    @staticmethod
    def convert_abfss_to_https_path(
        abfss_path: str, data_product_id: str, environment: str
    ) -> str:
        """Converts abfs path to https path

        Args:
            abfss_path (str): abfss path

        Returns:
            str: https path
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("convert_abfss_to_https_path"):
            try:
                # Use os.path.normpath() to normalize the path and handle both slashes
                normalized_path = os.path.normpath(abfss_path)

                # Split the path using the separator (either / or \) and get the hostname
                hostname = normalized_path.split(os.sep)[1]

                file_system = hostname.split("@")[0]
                logger.info(f"hostname:{hostname}")
                logger.info(f"file_system:{file_system}")
                storage_account = hostname.split("@")[1]
                logger.info(f"storage_account:{storage_account}")
                https_path = abfss_path.replace(
                    hostname, storage_account + "/" + file_system
                )
                https_path = https_path.replace("abfss", "https")

                # Replace backslashes with forward slashes for uniformity
                https_path = https_path.replace("\\", "/")

                # Check if the path starts with a valid URL scheme
                if not https_path.startswith("http://") and not https_path.startswith(
                    "https://"
                ):
                    https_path = (
                        "https://" + https_path
                    )  # Add "https://" as the default scheme
                else:
                    # Correct double "https://" occurrences
                    https_path = https_path.replace("https://https:/", "https://")
                    https_path = https_path.replace("https://https://", "https://")

                return https_path

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def file_exists(
        cls,
        running_local: bool,
        path: str,
        data_product_id: str,
        environment: str,
        dbutils=None,
        client_id: str = None,
        client_secret: str = None,
        tenant_id: str = None,
    ) -> bool:
        """
        Check if a file exists at the specified path.

        Args:
            running_local (bool): Indicates if the code is running locally.
            path (str): The path of the file to check.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the code is running.
            dbutils (optional): The dbutils object for Databricks. Defaults to None.
            client_id (str, optional): The client ID for authentication. Defaults to None.
            client_secret (str, optional): The client secret for authentication. Defaults to None.
            tenant_id (str, optional): The tenant ID for authentication. Defaults to None.

        Returns:
            bool: True if the file exists, False otherwise.
        """

        username = "unknown"
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("file_exists"):
            
            try:
                
                logger.info(
                    f"test if path exists: {path}"
                )
                                        
                if running_local is True:
                    if path.startswith("abfss://"):
                        try:
                            credential = ClientSecretCredential(
                                tenant_id, client_id, client_secret
                            )

                            https_path = cls.convert_abfss_to_https_path(
                                path, data_product_id, environment
                            )

                            storage_account_loc = urlparse(https_path).netloc
                            account_url = f"https://{storage_account_loc}"
                            storage_path = urlparse(https_path).path
                            storage_path_list = storage_path.split("/")
                            storage_container = storage_path_list[1]
                            file_path = storage_path.lstrip("/")
                            if file_path.startswith(f"{storage_container}/"):
                                file_path = file_path.replace(
                                    f"{storage_container}/", "", 1
                                )

                            logger.info(f"storage_path:{storage_path}")
                            logger.info(f"https_path:{https_path}")
                            logger.info(f"path:{path}")
                            service_client = DataLakeServiceClient(
                                account_url=account_url, credential=credential
                            )
                            file_system_client = service_client.get_file_system_client(
                                storage_container
                            )
                            file_client = file_system_client.get_file_client(file_path)
                            try:
                                file_exists = file_client.exists()
                                logger.info(
                                f"file_path{file_path}:file_exists:{file_exists}"
                                ) 
                                return file_exists
                            except HttpResponseError as e:
                                logger.error("HTTP response error: %s", e.message)
                                logger.error("ErrorCode: %s", e.error_code)
                                raise
                            except Exception as e:
                                logger.error("Unexpected error: %s", str(e))
                                raise
                            
                        except Exception as e:
                            raise
                    else:
                        return os.path.exists(path)
                else:
                            
                    try:
                        # Code that might throw an error
                        username = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
                    except Exception as e:
                        # Handling the error and defaulting to "unknown"
                        username = "unknown"
                        logger.info(f"Error: {e}")

                    logger.info(f"username: {username}")
                    
                    try:
                        if dbutils is not None:
                            if path.startswith("abfss://"):
                                # Check if the file exists using dbutils.fs.ls() for ABFSS paths
                                try:
                                    dbutils.fs.ls(path)
                                    b_exists = True  # File exists
                                except Exception as e:
                                    # If an exception is caught here, it typically means the file does not exist
                                    if "java.io.FileNotFoundException" in str(e):
                                        b_exists = False
                                    else:
                                        # Log the error and raise it if it's not a FileNotFoundException
                                        logger.error(f"Unexpected error while checking if file exists: {e}")
                                        raise
                            else:
                                # If not an ABFSS path, assume it's a local or another supported path type
                                path = path.replace("/dbfs", "")  # Adjust the path if necessary
                                try:
                                    with open(path, "rb") as f:
                                        # Read the first 10 bytes
                                        first_few_bytes = f.read(10)
                                        logger.info(f"First few bytes: {first_few_bytes}")
                                        b_exists = True  # If this line is reached, the file exists
                                except Exception as exception_result:
                                    logger.error(f"error in test as username:{username} if path exists: {path}")
                                    if "java.io.FileNotFoundException" in str(exception_result):
                                        b_exists = False
                                    else:
                                        b_exists = False
                                        raise
                        else:
                            b_exists = False
                            logger.info("dbutils is not available.")
                    except Exception as exception_result:
                        logger.error(f"error in test as username:{username} if path exists: {path}")
                        b_exists = False  # Set to False as default unless proven otherwise
                        raise exception_result
                    
                return b_exists
            except Exception as ex:
                logger.error(f"error in test as username:{username} if path exists: {path}")                        
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def copy_url_to_blob(
        cls,
        config: dict,
        src_url: str,
        dest_path: str,
        file_name: str,
        data_product_id: str,
        environment: str,
    ) -> str:
        """
        Downloads a file from the source URL and uploads it to the specified path in Azure Storage.

        Args:
            config (dict): The configuration dictionary containing the necessary Azure Storage parameters.
            src_url (str): The source URL from which to download the file.
            dest_path (str): The destination path in Azure Storage where the file will be uploaded.
            file_name (str): The name to be given to the file when it is uploaded to Azure Storage.

        Returns:
            str: A message indicating the status of the upload.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("copy_url_to_blob"):
            try:
                dest_path = cls.fix_url(dest_path, data_product_id, environment)
                info_message = f"copy_url_to_blob: src_url:{src_url}, dest_path:{dest_path}, file_name:{file_name}"
                logger.info(info_message)

                client_id = config["az_sub_client_id"]
                client_secret = config["client_secret"]
                tenant_id = config["az_sub_tenant_id"]
                if client_secret is None:
                    az_sub_client_secret_key = str(config["az_sub_client_secret_key"])
                    message = (
                        f"Environment variable: {az_sub_client_secret_key} not found"
                    )
                    client_secret = message
                    logger.info(client_secret)
                credential = ClientSecretCredential(tenant_id, client_id, client_secret)
                storage_account_loc = urlparse(dest_path).netloc
                storage_path = urlparse(dest_path).path
                storage_path_list = storage_path.split("/")
                storage_container = storage_path_list[1]
                account_url = f"https://{storage_account_loc}"
                service_client = DataLakeServiceClient(
                    account_url=account_url, credential=credential
                )
                os.environ["AZCOPY_SPA_CLIENT_SECRET"] = client_secret
                dir_path = storage_path.replace(f"{storage_container}" + "/", "")
                logger.info(f"dir_path:{dir_path}")
                file_system_client = service_client.get_file_system_client(
                    storage_container
                )
                directory_client = file_system_client.get_directory_client(dir_path)

                obj_http = EnvironmentHttp()
                http_headers = {}
                params = {}
                file_response = obj_http.get(
                    src_url, http_headers, 120, params, data_product_id, environment
                )

                if file_response.status_code != 200:
                    # Raise an exception if the status code is not 200 (OK)
                    file_response.raise_for_status()

                file_data = file_response.content
                try:
                    file_client = directory_client.create_file(file_name)
                    result = file_client.upload_data(
                        file_data, overwrite=True, max_concurrency=5
                    )
                except Exception as ex:
                    print(ex)
                    error_msg = "Error: %s", ex
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    result = "upload failed"
                return result

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def fix_url(path: str, data_product_id: str, environment: str):
        """
        Fixes the URL by replacing backslashes with forward slashes and adding the default scheme "https://" if necessary.

        Args:
            path (str): The URL path to be fixed.

        Returns:
            str: The fixed URL path.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("fix_url"):
            try:
                original_url = path
                # Replace backslashes with forward slashes for uniformity
                path = path.replace("\\", "/")

                # Check if the path starts with a valid URL scheme
                if not path.startswith("http://") and not path.startswith("https://"):
                    path = "https://" + path  # Add "https://" as the default scheme
                else:
                    # Correct double "https://" occurrences
                    path = path.replace("https://https:/", "https://")
                    path = path.replace("https://https://", "https://")

                # Validate the URL
                parsed_url = urlparse(path)
                if not parsed_url.scheme or not parsed_url.netloc:
                    raise ValueError(
                        f"Invalid URL: original_url: {original_url}, parsed_url {parsed_url}"
                    )

                logger.info(f"original_url:{original_url}")
                logger.info(f"parsed_url:{parsed_url}")
                logger.info(f"path:{path}")
                return path

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

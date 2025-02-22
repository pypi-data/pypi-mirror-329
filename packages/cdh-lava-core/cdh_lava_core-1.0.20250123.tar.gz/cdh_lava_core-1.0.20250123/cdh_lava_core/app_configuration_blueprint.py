import sys
import os
from flask_restx import Resource, fields, reqparse, Api
from werkzeug.datastructures import FileStorage
from flask import Blueprint, request, make_response
from flask import jsonify
from flask import render_template
import time
from cdh_lava_core.excel_service.excel_config_uploader import ExcelConfigUploader
from cdh_lava_core.excel_service.excel_sheet_combiner import ExcelSheetCombiner 
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
from cdh_lava_core.app_security_blueprint import role_required, azure_ad_authentication, get_required_role
from cdh_lava_core.app_orchestration_blueprint import list_config_environments
import traceback
import pandas as pd
from requests.exceptions import RequestException
from cdh_lava_core.app_shared_dependencies import get_config
from cdh_lava_core.az_storage_service.az_storage_file import AzStorageFile
import csv

cdh_configuration_bp = Blueprint('cdh_configuration', __name__)

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
ENVIRONMENT = "dev"

api = Api(cdh_configuration_bp)  # Initialize Api with the blueprint

upload_codes_form_parser = api.parser()
upload_codes_form_parser.add_argument(
    "file", location="files", type=FileStorage, required=True
)
upload_codes_form_parser.add_argument(
    "data_product_id", location="form", type=str, required=True
)
upload_codes_form_parser.add_argument(
    "environment", location="form", type=str, required=True
)


def format_time(seconds):
    """
    Format time in seconds to a string in the format HH:MM:SS.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


class MetadataExcelFileUploadCodes(Resource):
    """
    A Flask-RESTful resource for handling the upload_Codes of metadata Excel files.

    This class corresponds to the endpoint '/metadata_excel_file_upload'.
    It handles HTTP requests for uploading metadata Excel files.
    Each method in this class corresponds to a specific HTTP
    method (e.g., POST) and carries out the upload operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.

    Returns:
        Response: The response of the HTTP request after processing the
        uploaded file. The specific content and status code of the response
        will depend on the implementation.
    """


 
    @api.expect(upload_codes_form_parser, validate=True)
    @role_required(get_required_role)
    #@azure_ad_authentication
    def post(self, data_product_id):
        """
        Handles the HTTP POST request for uploading and processing an Excel file.
        This method performs the following steps:
        1. Initializes logging and tracing.
        2. Parses the uploaded file and reads its contents.
        3. Determines the repository path and ensures the necessary directories exist.
        4. Writes the uploaded file contents to a specified path.
        5. Combines sheets from the uploaded Excel file and saves the result as a CSV.
        6. Copies the CSV file to Azure Data Lake Storage.
        7. Returns a JSON response with trace ID, total processing time, and file path.
        Returns:
            Response: A Flask response object containing a JSON message with trace ID, total processing time, and file path.
        Raises:
            PermissionError: If there are permission issues while accessing files or directories.
            RequestException: If there is an issue with the request processing.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()
        
        with tracer.start_as_current_span("metadata_excel_file_upload_codes") as span:
            try:
                start_time = time.time()  # Record the start time

                trace_id = span.context.trace_id  # Correct way to access trace_id from the active span
                trace_id_hex = format(trace_id, '032x')  # 32-character hexadecimal string

                # Get the uploaded file
                config = get_config()
    
                
                args = upload_codes_form_parser.parse_args()
                file = args["file"]
                # Read the contents of the file as JSON
                file_contents = file.read()
                data_product_id = args["data_product_id"]
                obj_excel_config_uploader = ExcelConfigUploader()
                repository_path = config.get("repository_path")

                current_file_path = os.path.abspath(__file__)
                current_directory = os.path.dirname(current_file_path)
                logger.info(f"current_directory: {current_directory}")
                # Set repository_path to the premier_rep directory that is a peer of the current directory
                repository_path = os.path.join(current_directory, "../")

                # Ensure the path is absolute and normalized
                repository_path = os.path.abspath(repository_path)

                logger.info(f"repository_path:{repository_path}")
                environment = config.get("environment")
                authenticated_user_id = request.cookies.get("user_id", "unknown")

                manifest_excel_file_path_temp = (
                    obj_excel_config_uploader.get_excel_config_file_path(
                        repository_path,
                        data_product_id,
                        environment,
                        authenticated_user_id,
                    )
                )

                # Get the directory path without the file name
                directory_path = os.path.dirname(manifest_excel_file_path_temp)
                directory_path = directory_path.replace(
                    "/home/nfs/cdc/", "/home/nfs/CDC/"
                )

                # Log the action of creating directories
                logger.info(f"Ensure directory exists: {directory_path}")

                manifest_excel_file_path_temp = manifest_excel_file_path_temp.replace(
                    "/home/nfs/cdc/", "/home/nfs/CDC/"
                )

                # Create the directory if it does not exist
                os.makedirs(directory_path, exist_ok=True)

                with open(manifest_excel_file_path_temp, "ab") as f:
                    # Log the file open action
                    logger.info(
                        f"File opened successfully: {manifest_excel_file_path_temp}"
                    )

                directory_path = os.path.dirname(manifest_excel_file_path_temp)

                # Log the action of creating directories
                logger.info(f"Ensure directory exists: {directory_path}")

                # Create the directory if it does not exist
                os.makedirs(directory_path, exist_ok=True)

                with open(manifest_excel_file_path_temp, "ab") as f:
                    # Log the file open action
                    logger.info(
                        f"File opened successfully: {manifest_excel_file_path_temp}"
                    )
                    f.write(file_contents)

                obj_excel_sheet_combiner = ExcelSheetCombiner()

                result_df = obj_excel_sheet_combiner.combine_sheets(manifest_excel_file_path_temp, data_product_id, environment)
                base_path = os.path.dirname(manifest_excel_file_path_temp)
                source_path = os.path.join(base_path, data_product_id + '_code_local_valuesets.csv')

                # Add debug logging for the source_path
                logger.info(f"Attempting to save to source_path: {source_path}")

                # Check if the directory exists
                directory = os.path.dirname(source_path)
                if not os.path.exists(directory):
                    logger.error(f"Directory does not exist: {directory}")
                    raise OSError(f"Cannot save file to a non-existent directory: {directory}")

                # Try writing to CSV and catch any errors
                try:
                    logger.info(f"Resulting DataFrame: {result_df.head()}")  # Log first few rows of the DataFrame
                    result_df.to_csv(source_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
                    logger.info(f"File successfully saved to: {source_path}")
                except Exception as e:
                    logger.error(f"Failed to save CSV to {source_path}: {str(e)}")
                
                destination_path = f"https://edavcdhproddlmprd.dfs.core.windows.net/cdh/raw/lava/{data_product_id}/data/local/{data_product_id}_code_local_valuesets.csv"
                from_to = "LocalBlobFS"

                # Call the method
                obj_storage_file = AzStorageFile()
                dbutils=None
                result = obj_storage_file.file_adls_copy(
                config, source_path, destination_path, from_to, dbutils, data_product_id, environment
                )

                end_time = time.time()  # Record the end time

                total_time = end_time - start_time  # Calculate the total time
                total_time_string = format_time(total_time)

                # Create the return message with the start, end, and total time
                message = {
                    "trace_id": trace_id_hex,
                    "total_time": total_time_string,
                    "data": "Success",
                    "file_path" : manifest_excel_file_path_temp
                }

                 
                response = make_response(jsonify(message), 200)
                # Set up custom CORS headers

                return response

            except PermissionError as ex:
                # Return a 403 Forbidden status if permissions are denied
                msg = f"Permission denied: {str(ex)}"
                logger.warning(msg)
                return jsonify({"error": msg}), 403
                
            except RequestException as ex:
                msg = f"RequestException occurred: {str(ex)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                # Create the return message with the start, end, and total time
                message = {"data": msg}

                return jsonify(message), 500

    @azure_ad_authentication
    def get(self, data_product_id):
        """
        Handles the upload of codes for a given data product.
        This function performs the following steps:
        1. Logs the full request URL and the provided data product ID.
        2. Constructs the path to the CSV file containing the codes.
        3. Reads the CSV file into a pandas DataFrame.
        4. Converts the DataFrame to a list of dictionaries.
        5. Lists the configuration environments from the CSV directory.
        6. Renders the upload codes template with the necessary data.
        Args:
            data_product_id (str): The ID of the data product for which codes are being uploaded.
        Returns:
            str: Rendered HTML template for uploading codes or an error page if an exception occurs.
        Raises:
            ValueError: If `parent_dir` or `data_product_id` is None.
            Exception: If any other unexpected error occurs during the process.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()
        
            
        with tracer.start_as_current_span("upload_codes"):
            try:

                calling_page_url = request.url
                logger.info(f"Full request URL: {request.url}")

                logger.info(f"data_product_id: {data_product_id}")

                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                # Go up one directory from the current directory
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
                # Construct the relative path to the CSV file
                if parent_dir   is None:
                    raise ValueError("parent_dir is None, cannot construct path.")
                if data_product_id   is None:
                    raise ValueError("data_product_id is None, cannot construct path.")
                csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
                csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_jobs.csv")
                logger.info(f"csv_path:{csv_path}")
                df = pd.read_csv(csv_path)
                # Convert the DataFrame to a list of dictionaries
                data = df.to_dict(orient="records")
                logger.info(f"data: {data}")
                config_environments = list_config_environments(csv_directory_path)
                logger.info(f"data_product_id: {data_product_id}")  # Debugging line
                return make_response(render_template(
                    "data_products/upload_codes.html",
                    data_product_id=data_product_id,
                    calling_page_url=calling_page_url,
                    environments=config_environments,
                ))
            except Exception as ex:
                trace_msg_error = traceback.format_exc()
                exc_line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {exc_line_number}\nCall Stack:{trace_msg_error}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    SERVICE_NAME, NAMESPACE_NAME, data_product_id, ENVIRONMENT
                ).error_with_exception(error_message, exc_info)
                return make_response(render_template("error.html", error_message=error_message))




class PermissionError(Exception):
    pass

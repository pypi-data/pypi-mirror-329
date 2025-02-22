
import cdh_lava_core.alation_service.db_schema as alation_schema
from flask_restx import Resource, fields, reqparse

class MetadataJsonFileDownload(Resource):
    """
    A Flask-RESTful resource responsible for downloading metadata JSON files.

    This class handles HTTP requests to the corresponding endpoint. It likely
    implements methods such as GET to handle the downloading of a metadata
    JSON file. Each method corresponds to a standard HTTP method
    (e.g., GET, POST, PUT, DELETE) and carries out a specific operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.
    """

    def get(self, schema_id):
        """
        Retrieves the JSON metadata file from Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            JSON file.

        Returns:
            dict: A dictionary containing the downloaded JSON metadata file.

        Example:
            Use schema_id 106788 to test LAVA_CORE_PROD (DataBricks): lava_core_prod
            Use schema_id 1464 to test Acme Bookstore (Synapse SQL Warehouse): EDAV.alation
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("metadata_json_file_download"):
            try:
                start_time = time.time()  # Record the start time

                config = app.cdc_config

                schema = alation_schema.Schema()
                manifest_json_file = schema.download_manifest_json(schema_id, config)

                # Return the file as a download_edc
                file_name = os.path.basename(manifest_json_file)

                end_time = time.time()  # Record the start time

                total_time = end_time - start_time  # Calculate the total time

                logger.info("Successfully downloaded the JSON metadata file.")
                # Return the file as a response
                return send_file(
                    manifest_json_file,
                    as_attachment=True,
                    download_name=file_name,
                )

            except Exception as ex_download:
                msg = f"An unexpected error occurred for download_edc file for schema_id: {schema_id}: {str(ex_download)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
                ).force_flush()
                response = make_response(jsonify({"error": msg}), 500)
                return response


class MetadataExcelFileDownloadEdc(Resource):
    """
    A Flask-RESTful resource responsible for handling requests for downloading
    metadata Excel files with a specific schema id.

    This class corresponds to the endpoint
    '/metadata_excel_file_download/<int:schema_id>'.
    It handles HTTP requests that include a specific schema id in the URL, and
    it likely implements methods like GET to manage the download_edc of the
    associated metadata Excel file.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating
        new RESTful resources.
    """

    def get(self, schema_id):
        """
        Retrieves the Excel metadata file from Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the downloaded Excel metadata file.

        Example:
            Use schema_id 106788TBD to test LAVA_CORE_PROD (DataBricks): lava_core_prod
            Use schema_id 1464 to test Acme Bookstore (Synapse SQL Warehouse): EDAV.alationn
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
        ).initialize_logging_and_tracing()
        
        azure_trace_exporter = tracer.azure_trace_exporter

        with tracer.start_as_current_span(
            f"metadata_excel_file_download_edc/{schema_id}"
        ):
            try:

                start_time = time.time()  # Record the start time

                config = app.cdc_config

                obj_file = cdc_env_file.EnvironmentFile()
                app_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(app_dir)

                repository_path = config.get("repository_path")
                environment = config.get("environment")

                schema = alation_schema.Schema()
                excel_data_definition_file = schema.get_excel_data_definition_file_path(
                    repository_path, environment
                )
                manifest_excel_file = schema.download_manifest_excel(
                    schema_id,
                    config,
                    excel_data_definition_file,
                    DATA_PRODUCT_ID
                )

                # Return the file as a download_edc
                file_name = os.path.basename(manifest_excel_file)
                logger.info(f"file_name:{file_name}")

                end_time = time.time()  # Record the start time

                total_time = end_time - start_time  # Calculate the total time

                # Create the return message with the start, end, and total time
                message = {
                    "start_time": start_time,
                    "end_time": end_time,
                    "total_time": total_time,
                    "data": "Success",
                }

                mime_type = "application/vnd.openxmlformats"
                mime_type = mime_type + "-officedocument.spreadsheetml.sheet"

                # Return the file as a response
                return send_file(
                    manifest_excel_file,
                    as_attachment=True,
                    download_name=file_name,
                )

            except Exception as ex:
                msg = f"An unexpected error occurred for download_edc file for schema_id: {schema_id}: {str(ex)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
                ).force_flush()
                response = make_response(jsonify({"error": str(ex)}), 500)
                return response
            finally:
                # Ensure that all telemetry is flushed to Application Insights before the process ends
                azure_trace_exporter.flush()  # Force flush telemetry


class MetadataExcelFileUploadEdc(Resource):
    """
    A Flask-RESTful resource for handling the upload_edc of metadata Excel files.

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

    @api.expect(upload_parser_edc, validate=True)
    @azure_ad_authentication
    def post(self):
        """
        Uploads the Excel metadata file to Alation via direct upload_edc based on
        the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the response data.

        Example:
            Use schema_id 106788 to test LAVA_CORE_PROD (DataBricks): lava_core_prod
            Use schema_id 1464 to test Acme Bookstore (Synapse SQL Warehouse): EDAV.alation
        """

        with tracer.start_as_current_span("metadata_excel_file_upload_edc"):
            try:
                start_time = time.time()  # Record the start time

                # Get the uploaded file
                args = upload_parser_edc.parse_args()
                file = args["file"]
                # Read the contents of the file as JSON
                file_contents = file.read()

                schema = alation_schema.Schema()
                repository_path = config.get("repository_path")
                environment = config.get("environment")
                alation_user_id = 7

                manifest_excel_file_path_temp = (
                    schema.get_excel_manifest_file_path_temp(
                        "upload_edc", repository_path, environment, alation_user_id
                    )
                )

                with open(manifest_excel_file_path_temp, "wb") as f:
                    f.write(file_contents)

                schema_json_file_path = schema.get_json_data_definition_file_path(
                    repository_path, environment
                )

                authenticated_user_id = request.cookies.get("user_id")

                (
                    content_result,
                    authorized_tables_count,
                    unauthorized_table_count,
                ) = schema.upload_edc_manifest_excel(
                    manifest_excel_file_path_temp,
                    config,
                    schema_json_file_path,
                    authenticated_user_id,
                )

                logger.info(f"content_result: {content_result}")

                end_time = time.time()  # Record the end time

                total_time = end_time - start_time  # Calculate the total time
                total_time_string = format_time(total_time)

                # Create the return message with the start, end, and total time
                message = {
                    "total_time": total_time_string,
                    "authorized_tables_count": authorized_tables_count,
                    "unauthorized_table_count": unauthorized_table_count,
                    "data": "Success",
                }

                response = make_response(jsonify(message), 200)
                # Set up custom CORS headers

                return response

            except RequestException as ex:
                msg = f"RequestException occurred: {str(ex)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                # Create the return message with the start, end, and total time
                message = {"data": msg}

                response = make_response(jsonify(message), 500)
                return response


class MetadataJsonFileUploadEdc(Resource):
    """
    A Flask-RESTful resource for handling the upload_edc of metadata JSON files.

    This class corresponds to the endpoint '/metadata_json_file_upload_edc'. It
    handles HTTP requests for upload_edcing metadata JSON files.
    Each method in this class corresponds to a specific HTTP
    method (e.g., POST) and carries out the upload operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.

    Returns:
        Response: The response of the HTTP request after processing the
        uploaded file.
        The specific content and status code of the response will depend on
        the implementation.
    """

    @api.expect(upload_parser_edc, validate=True)
    @azure_ad_authentication
    def post(self):
        """Uploads JSON metadata file via direct upload to Alation
        based on schema_id.
        Use 106788 to test LAVA_CORE_PROD (DataBricks)
        """

        with tracer.start_as_current_span("metadata_json_file_upload_edc"):
            try:
                start_time = time.time()  # Record the start time

                # Get the uploaded file
                args = upload_parser_edc.parse_args()
                file = args["file"]
                # Read the contents of the file as JSON
                file_contents = file.read()
                metadata_json_data = json.loads(file_contents)

                schema = alation_schema.Schema()
                config = app.cdc_config

                repository_path = config.get("repository_path")
                environment = config.get("environment")
                json_data_definition_file_path = (
                    schema.get_json_data_definition_file_path(
                        repository_path, environment, DATA_PRODUCT_ID
                    )
                )

                authenticated_user_id = request.cookies.get("user_id")

                (
                    content_result,
                    authorized_tables_count,
                    unauthorized_table_count,
                ) = schema.upload_manifest_json(
                    metadata_json_data, config, authenticated_user_id
                )

                logger.info(f"content_result: {content_result}")

                end_time = time.time()  # Record the end time

                total_time = end_time - start_time  # Calculate the total time

                # Create the return message with the start, end, and total time
                message = {
                    "total_time": total_time,
                    "authorized_tables_count": authorized_tables_count,
                    "unauthorized_table_count": unauthorized_table_count,
                    "data": "Success",
                }

                response = make_response(jsonify(message), 200)
                return response

            except RequestException as ex:
                msg = f"RequestException occurred: {str(ex)}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(msg, exc_info)
                # Create the return message with the start, end, and total time
                message = {
                    "start_time": start_time,
                    "end_time": end_time,
                    "total_time": total_time,
                    "data": msg,
                }

                response = make_response(jsonify(message), 500)
                return response


upload_parser_edc = api.parser()
upload_parser_edc.add_argument(
    "file", location="files", type=FileStorage, required=True
)

# This model is used for swagger documentation
ns_alation.add_resource( MetadataJsonFileDownload, "/metadata_json_file_download/<int:schema_id>")
ns_alation.add_resource(MetadataExcelFileDownloadEdc, "/metadata_excel_file_download_edc/<int:schema_id>")
ns_alation.add_resource(MetadataJsonFileUploadEdc, "/metadata_json_file_upload_edc")
ns_alation.add_resource(MetadataExcelFileUploadEdc, "/metadata_excel_file_upload_edc")


@cdc_files_protected_bp.route("/upload_edc")
def upload_edc():
    calling_page_url = request.args.get("calling_page")
    return render_template("data_products/upload_edc.html", calling_page_url=calling_page_url)


@cdc_files_bp.route("/download_edc")
def download_edc():
    calling_page_url = request.args.get("calling_page")
    return render_template("download_edc.html", calling_page_url=calling_page_url)



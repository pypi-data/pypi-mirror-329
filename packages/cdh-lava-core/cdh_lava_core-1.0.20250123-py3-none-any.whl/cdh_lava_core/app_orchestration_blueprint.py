import sys
import os
from flask_restx import Resource, fields, Api
from flask import (
    redirect,
    send_file,
    request,
    render_template,
    Blueprint,
    jsonify,
    make_response,
    url_for,
    session,
    flash,
    Response,
    json
)


from flask_restx import Namespace, Resource, fields
import traceback
from datetime import datetime
import time
import pandas as pd
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
from cdh_lava_core.databricks_service.dbx_db_rest import RestClient
from cdh_lava_core.databricks_service.dbx_db_rest.jobs import JobsClient
from dotenv import load_dotenv
from requests.exceptions import RequestException
from collections import OrderedDict

cdh_orchestration_bp = Blueprint('cdh_orchestration', __name__)

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
api = Api(cdh_orchestration_bp)  # Initialize Api with the blueprint
ENVIRONMENT = "dev"  # Set the environment name
DATA_PRODUCT_ID = "lava_core"

job_run_parser = api.parser()
job_run_parser.add_argument(
    "environment", location="form", type=str, required=True
)
job_run_parser.add_argument(
    "data_product_id", location="form", type=str, required=True
)
job_run_parser.add_argument(
    "job_name", location="form", type=str, required=True
)
job_run_parser.add_argument(
    "lava_admin_user_or_role", location="form", type=str, required=True
)

# Define the model for the response data (if needed for Swagger)
data_product_model = api.model('DataProductModel', {
    'data_product_id': fields.String(description='ID of the data product', required=True),
    'data_product_name': fields.String(description='Name of the data product', required=True),
    # Add other relevant fields that correspond to the CSV structure
})


def list_config_environments(directory):
    """
    Extracts the middle parts of filenames in a directory that match the pattern 'config.*.json'.

    Args:
        directory (str): The directory to search for files.

    Returns:
        list: A list of middle parts extracted from filenames that match the pattern.
    """
    middle_parts = []

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Check if the filename starts with 'config.' and ends with '.json'
        if filename.startswith('config.') and filename.endswith('.json'):
            # Extract the middle part (the part between 'config.' and '.json')
            middle_part = filename[len('config.'):-len('.json')]
            middle_parts.append(middle_part)
    
    return middle_parts


class DataProductsData(Resource):
    """
    DataProductsData is a Flask-RESTful resource that handles HTTP GET requests to retrieve data from a CSV file and return it in JSON format.
    Methods:
        get():
            Retrieves data from a CSV file located in the parent directory of the current file's directory.
            Converts the CSV data into a list of dictionaries and returns it as a JSON response.
            Optionally retrieves the 'calling_page' parameter from the request arguments.
    Attributes:
        None
    """
    @api.doc(description="Get CDC queries data from a CSV file")
    @api.marshal_with(data_product_model, as_list=True)
    def get(self):
        """
        Retrieves data from a CSV file and returns it in JSON format.
        """
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        csv_path = os.path.join(parent_dir, "lava_core", "bronze_data_products.csv")

        # Read the CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient="records")

        # You can still retrieve other parameters if needed (though not rendered)
        calling_page_url = request.args.get("calling_page")

        # Return the data as a JSON response
        return data, 200


class DataProductsForJobs(Resource):
    @api.doc(
        description="Returns data products and renders an HTML page with the data.",
        params={
            'calling_page': {'description': 'URL of the calling page', 'in': 'query', 'type': 'string'}
        },
        responses={
            200: 'HTML page with data rendered',
            400: 'Bad Request'
        }
    )
    def get(self):
        """Fetch and display data products."""
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Go up one directory from the current directory
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

            # Construct the relative path to the CSV file
            csv_path = os.path.join(parent_dir, "lava_core", "bronze_data_products.csv")

            df = pd.read_csv(csv_path)
            # Convert the DataFrame to a list of dictionaries
            data = df.to_dict(orient="records")

            calling_page_url = request.args.get("calling_page")

            html_content =  render_template(
                "data_products/data_products_home.html",
                calling_page_url=calling_page_url,
                data=data,
            )

            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html'
            return response

        except Exception as e:
            api.abort(400, f"Error loading data: {str(e)}")


class DataProductsForQueries(Resource):
    @api.doc(
        description="Returns data products and renders an HTML page with the data.",
        params={
            'calling_page': {'description': 'URL of the calling page', 'in': 'query', 'type': 'string'}
        },
        responses={
            200: 'HTML page with data rendered',
            400: 'Bad Request'
        }
    )
    def get(self):
        """Fetch and display data products."""
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Go up one directory from the current directory
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

            # Construct the relative path to the CSV file
            csv_path = os.path.join(parent_dir, "lava_core", "bronze_data_products.csv")

            df = pd.read_csv(csv_path)
            # Convert the DataFrame to a list of dictionaries
            data = df.to_dict(orient="records")

            calling_page_url = request.args.get("calling_page")

            html_content =  render_template(
                "queries/queries_home.html",
                calling_page_url=calling_page_url,
                data=data,
            )

            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html'
            return response

        except Exception as e:
            api.abort(400, f"Error loading data: {str(e)}")

# Define the expected model for incoming JSON data (for Swagger documentation)
query_model = api.model('QueryModel', {
    'database': fields.String(required=True, description='Database name'),
    'execute_flag': fields.String(required=True, description='Flag to execute the workflow', example='execute'),
    'execute_results_flag': fields.String(required=True, description='Flag to execute results', example='skip_execute'),
    'export_schema_metrics': fields.String(description='Export schema metrics', example=''),
    'workflow_batch_group': fields.String(required=True, description='Workflow batch group', example='3'),
    'workflow_description': fields.String(description='Workflow description', example=''),
    'workflow_name': fields.String(required=True, description='Name of the workflow', example='03_lava_core_viz_valueset_param'),
    'workflow_parameters': fields.String(description='Parameters for the workflow', example='viz_app_code:iddsldd|valueset_param:view_by'),
    'workflow_type': fields.String(required=True, description='Type of the workflow', example='databricks_sql'),
    'data_product_id': fields.String(required=True, description='ID of the data product', example='premier_iddsldd'),
    'row_id_keys': fields.String(description='Row ID keys', example=''),
    'save_flag': fields.String(description='Flag to save the workflow', example='save'),
    'view_name': fields.String(description='Name of the view', example='03_viz_code_viewby'),
    'workflow_category': fields.String(description='Workflow category', example='03_code_viz_lookups')
})

queries_model = api.model('QueriesModel', {
    'data': fields.List(fields.Nested(query_model), required=True, description='Array of query objects')
})

# Define the expected model for incoming JSON data (for Swagger documentation)
dataset_model = api.model('DatasetModel', {
    'column_header_skip_rows': fields.String(description='Column Header Skip Rows'),
    'column_ordinal_sort': fields.String(description='Column Ordinal Sort'),
    'compare_filter': fields.String(description='Compare Filter'),
    'compare_table': fields.String(description='Compare Table'),
    'crdy_domain': fields.String(description='CRDY Domain'),
    'crdy_is_sa_dataset': fields.String(description='CRDY is SA Dataset'),
    'crdy_maximum_latency_hours': fields.String(description='CRDY Maximum Latency Hours'),
    'crdy_subdomain': fields.String(description='CRDY Subdomain'),
    'crdy_subdomain2': fields.String(description='CRDY Subdomain 2'),
    'database': fields.String(description='Database'),
    'dataset_description': fields.String(description='Dataset Description'),
    'dataset_friendly_name': fields.String(description='Dataset Friendly Name'),
    'dataset_name': fields.String(description='Dataset Name'),
    'edc_access_level': fields.String(description='EDC Access Level'),
    'edc_alation_datasource_id': fields.String(description='EDC Alation Datasource ID'),
    'edc_alation_datasource_identifier': fields.String(description='EDC Alation Datasource Identifier'),
    'edc_alation_schema_id': fields.String(description='EDC Alation Schema ID'),
    'edc_applicability_end_date': fields.String(description='EDC Applicability End Date'),
    'edc_applicability_start_date': fields.String(description='EDC Applicability Start Date'),
    'edc_citation': fields.String(description='EDC Citation'),
    'edc_conform_to_standard': fields.String(description='EDC Conform To Standard'),
    'edc_homepage_url': fields.String(description='EDC Homepage URL'),
    'edc_identifier': fields.String(description='EDC Identifier'),
    'edc_is_containing_pii': fields.String(description='EDC is Containing PII'),
    'edc_language': fields.String(description='EDC Language'),
    'edc_license': fields.String(description='EDC Liscence'),
    'edc_pii_comments': fields.String(description='EDC PII Comments'),
    'edc_pii_fields': fields.String(description='EDC PII Fields'),
    'edc_reference': fields.String(description='EDC Reference'),
    'edc_referenced_by': fields.String(description='EDC Referenced By'),
    'edc_release_date': fields.String(description='EDC Release Date'),
    'edc_size': fields.String(description='EDC Size'),
    'edc_submitting_user': fields.String(description='EDC Submitting User'),
    'edc_tags': fields.String(description='EDC Tags'),
    'edc_update_frequency': fields.String(description='EDC Update Frequency'),
    'encoding': fields.String(description='Encoding'),
    'entity': fields.String(description='Entity'),
    'excluded_environments': fields.String(description='Excluded Environments'),
    'file_name': fields.String(description='File Name'),
    'folder_name': fields.String(description='Folder Name'),
    'folder_name_source': fields.String(description='Folder Name Source'),
    'format': fields.String(description='Format'),
    'frequency': fields.String(description='Frequency'),
    'incremental': fields.String(description='Incremental'),
    'is_active': fields.String(description='Is Active'),
    'is_export_schema_required': fields.String(description='Is Export Schema Required'),
    'is_multiline': fields.String(description='Is Multiline'),
    'is_refreshed': fields.String(description='Is Refreshed'),
    'is_required_for_power_bi': fields.String(description='Is Required For Power BI'),
    'optimize_columns': fields.String(description='Optimize Columns'),
    'optimize_type': fields.String(description='Optimize Type'),
    'pii_columns': fields.String(description='PII Columns'),
    'workflow_batch_group': fields.String(description='Workflow Batch Group'),
    'data_product_id': fields.String(description='Data Product ID'),
    'remove_columns_with_no_metadata': fields.String(description='Remove Columns With No Metadata'),
    'row_id_core_columns': fields.String(description='Row ID Core Columns'),
    'use_liquid_clustering': fields.String(description='Use Liquid Clustering'),
    'partition_by': fields.String(description='Partition By'),
    'row_id_keys': fields.String(description='Row ID Keys'),
    'sheet_name': fields.String(description='Sheet Name'),
    'source_abbreviation': fields.String(description='Source Abbreviation'),
    'source_dataset_name': fields.String(description='Source Dataset Name'),
    'source_json_path': fields.String(description='Source JSON Path')
})

datasets_model = api.model('DatasetsModel', {
    'data': fields.List(fields.Nested(dataset_model), required=True, description='Array of dataset objects')
})

@api.doc(params={'data_product_id': 'The ID of the data product to query'})
class QueriesList(Resource):
    @api.doc(description="Fetch and render the list of queries for a given data product ID.")
    @api.response(200, 'HTML Page rendered successfully')
    @api.response(500, 'Internal Server Error')
    def get(self, data_product_id):
        """
        Fetch and render the queries for the specified data product using make_response.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("queries_list_get"):
            try:
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                # Go up one directory from the current directory
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

                # Construct the relative path to the CSV file
                csv_directory_path = os.path.join(parent_dir, data_product_id, "config")
                csv_path = os.path.join(csv_directory_path, "bronze_sps_config_workflows.csv")
                logger.info(f"csv_path:{csv_path}")
                
                # Read the CSV into a DataFrame
                df = pd.read_csv(csv_path)

                # Replace NaN values with an empty string
                df = df.fillna(value='')

                # Convert the DataFrame to a list of dictionaries
                queries = df.to_dict(orient="records")

                # split workflow parameters into sub-lists for display
                for row in queries:
                    row["workflow_parameters"] = [param.split(":") for param in row["workflow_parameters"].split("|")]

                # Fetch environments (custom logic, assumes the function exists)
                environments = list_config_environments(csv_directory_path)

                # Use make_response to create a response object and modify headers if needed
                calling_page_url = request.url
                response = make_response(
                    render_template(
                        "queries/queries_list.html", 
                        calling_page_url=calling_page_url, 
                        queries=queries, 
                        environments=environments
                    )
                )
                
                # Optionally, you can modify the response headers or status code
                response.headers['Content-Type'] = 'text/html; charset=utf-8'
                response.status_code = 200
                
                return response

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                
                # Log the error if needed, and return an HTML error page
                logger.error(error_message, exc_info=sys.exc_info())
                response = make_response(
                    render_template("error.html", error_message=error_message), 
                    500
                )
                return response


    @api.expect(queries_model, validate=True)
    @api.doc(description="Update the queries CSV file with new data for a given data product.")
    @api.response(200, 'CSV file updated successfully')
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    def post(self, data_product_id):
        """
        Update the queries for the specified data product by modifying the CSV file on the server.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("queries_list_post"):
            try:
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                if not data_product_id:
                    return {"error": "Missing 'data_product_id' in request"}, 400

                # Construct the relative path to the CSV file
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
                csv_directory_path = os.path.join(parent_dir, data_product_id, "config")
                csv_path = os.path.join(csv_directory_path, "bronze_sps_config_workflows.csv")
                logger.info(f"csv_path: {csv_path}")

                # Expected columns in the DataFrame
                expected_columns = [
                    'database', 'execute_flag', 'execute_results_flag', 'export_schema_metrics',
                    'workflow_batch_group', 'workflow_description', 'workflow_name', 
                    'workflow_parameters', 'workflow_type', 'data_product_id', 'row_id_keys', 
                    'save_flag', 'view_name', 'workflow_category'
                ]

                # Get the data from the request JSON
                new_queries = request.json.get('data', [])
                if not new_queries:
                    return {"error": "No queries provided in 'data' array"}, 400

                logger.info(f"Received new query data: {new_queries}")

                # Convert new_queries list of dicts to a DataFrame
                new_queries_df = pd.DataFrame(new_queries)

                # Ensure new_queries_df has the required columns, filling in missing columns with empty strings
                for column in expected_columns:
                    if column not in new_queries_df.columns:
                        new_queries_df[column] = ''

                # Save the updated DataFrame back to the CSV
                os.makedirs(csv_directory_path, exist_ok=True)  # Ensure the directory exists
                new_queries_df.to_csv(csv_path, index=False)
                logger.info(f"CSV file updated successfully at {csv_path}")

                return {"message": "CSV file updated successfully"}, 200

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                
                # Log the error and return a 500 Internal Server Error
                logger.error(error_message, exc_info=True)
                return {"error": error_message}, 500



class DataProductsForDatasets(Resource):
    @api.doc(
        description="Returns data products and renders an HTML page with the data.",
        params={
            'calling_page': {'description': 'URL of the calling page', 'in': 'query', 'type': 'string'}
        },
        responses={
            200: 'HTML page with data rendered',
            400: 'Bad Request'
        }
    )
    def get(self):
        """Fetch and display data products."""
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Go up one directory from the current directory
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

            # Construct the relative path to the CSV file
            csv_path = os.path.join(parent_dir, "lava_core", "bronze_data_products.csv")

            df = pd.read_csv(csv_path)
            # Convert the DataFrame to a list of dictionaries
            data = df.to_dict(orient="records")

            calling_page_url = request.args.get("calling_page")

            html_content =  render_template(
                "datasets/datasets_home.html",
                calling_page_url=calling_page_url,
                data=data,
            )

            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html'
            return response

        except Exception as e:
            api.abort(400, f"Error loading data: {str(e)}")


def format_time(seconds):
    """
    Format time in seconds to a string in the format HH:MM:SS.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

class JobRun(Resource):
    @api.expect(job_run_parser, validate=True)
    # comment out for now TODO Fix
    # @azure_ad_authentication
    def post(self):

        # Get the uploaded file
        args = job_run_parser.parse_args()
        environment = args["environment"]
        data_product_id = args["data_product_id"]



        tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("job_run") as span:
            try:
                start_time = time.time()  # Record the start time

                trace_id = span.context.trace_id  # Correct way to access trace_id from the active span
                trace_id_hex = format(trace_id, '032x')  # 32-character hexadecimal string

                job_name = args["job_name"]
                lava_admin_user_or_role = args["lava_admin_user_or_role"]

                current_file_path = os.path.abspath(__file__)
                current_directory = os.path.dirname(current_file_path)
                logger.info(f"current_directory: {current_directory}")
                # Set repository_path to the premier_rep directory that is a peer of the current directory
                repository_path = os.path.join(current_directory, "../")

                # Ensure the path is absolute and normalized
                repository_path = os.path.abspath(repository_path)

                logger.info(f"repository_path:{repository_path}")
                authenticated_user_id = request.cookies.get("user_id", "unknown")
                current_dir = os.path.dirname(__file__)

                # Construct the path to the peer directory "lava_core" and the .env file inside it
                dotenv_path = os.path.join(os.path.dirname(current_dir), "lava_core", ".env")
                logger.info(f"dotenv_path:{dotenv_path}")
                # If the .env file in lava_core does not exist, fallback to the .env in the parent directory
                if not os.path.exists(dotenv_path):
                    dotenv_path = os.path.join(os.path.dirname(current_dir), ".env")
                logger.info(f"dotenv_file_path:{dotenv_path}")
                # Load the .env file
                load_dotenv(dotenv_path)
                token = os.getenv("CDH_LAVA_PROD_SPN_PAT")
                host = os.getenv("DATABRICKS_HOST")
                host = host.rstrip("/")

                config = {
                "data_product_id": data_product_id,
                "environment": environment,
                }

                logger.info(f"host: {host}")

                rest_client = RestClient(token, host, config=config)
                jobs_client = JobsClient(rest_client)
                two_digit_month = datetime.now().strftime("%m")
                full_job_name = f"{data_product_id}_{job_name}_{environment}"
                # Arrange
                params = {
                    "existing_cluster_id": "0109-184947-l0ka6b1y",  # Replace with your actual cluster ID
                    "name": full_job_name,  # Job name
                    "notebook_task": {
                        "notebook_path": f"/Repos/CDH_LAVA/cdh-lava-core-main/{data_product_id}/_run_jobs_{data_product_id}",  # Path to your Python notebook in Databricks
                        "base_parameters": {
                            "job_name": job_name,  # Add the job_name parameter
                            "report_dd": "NA",  # Add the report_dd parameter
                            "report_mm": two_digit_month,  # Add the report_mm parameter
                            "report_yyyy": "2024",  # Add the report_yyyy parameter
                        },
                    },
                }

                # Act
                params['lava_admin_user_or_role'] = lava_admin_user_or_role
                result = jobs_client.create(params, run_now=True)

                end_time = time.time()  # Record the end time

                total_time = end_time - start_time  # Calculate the total time
                total_time_string = format_time(total_time)

                # Create the return message with the start, end, and total time
                message = {
                    "trace_id": trace_id_hex,
                    "total_time": total_time_string,
                    "data": "Success"
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

@cdh_orchestration_bp.route("/cdh_orchestration/data_product_job/<data_product_id>")
def data_product_job(data_product_id):

    tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
    ).initialize_logging_and_tracing()
    
    with tracer.start_as_current_span("data_product_job"):
        try:

            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Go up one directory from the current directory
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

            # Construct the relative path to the CSV file
            csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
            csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_jobs.csv")
            logger.info(f"csv_path:{csv_path}")
            df = pd.read_csv(csv_path)
            # Convert the DataFrame to a list of dictionaries
            data = df.to_dict(orient="records")
            jobs = []
            for row in data:
                jobs.append({'job': row['job'], 'lava_admin_user_or_role': row['lava_admin_user_or_role']})  # Extract 'job' and 'lava_admin_user_or_role'
            calling_page_url = request.url
            environments = list_config_environments(csv_directory_path)
            return render_template(
                "data_products/data_product_job.html", calling_page_url=calling_page_url, jobs=jobs, environments=environments
            )
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            exc_info = sys.exc_info()
            LoggerSingleton.instance(
                SERVICE_NAME, NAMESPACE_NAME, data_product_id, ENVIRONMENT
            ).error_with_exception(error_message, exc_info)
            return render_template("error.html", error_message=error_message)

@cdh_orchestration_bp.route("/environments", endpoint='environments_list')
def environments():

    tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
    ).initialize_logging_and_tracing()
    
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file containing data products
    data_products_csv_path = os.path.join(parent_dir, "lava_core", "bronze_data_products.csv")

    # Read the CSV file to get the list of data products
    df_data_products = pd.read_csv(data_products_csv_path)
    
    # Initialize an empty list to store all data product-environment combinations
    combined_list = []

    # Loop through each data product
    for _, row in df_data_products.iterrows():
        data_product_id = row['data_product_id']  # Assuming 'data_product_id' is a column in the CSV

        # Construct the path to the environment config directory for each data product
        config_directory_path = os.path.join(parent_dir, data_product_id, "config")

        # Retrieve the list of environments for this data product
        config_environments = list_config_environments(config_directory_path)

        # For each environment, append a dictionary with the data product and environment combination
        for environment in config_environments:
            combined_list.append({
                'data_product_id': data_product_id,
                'environment': environment
            })

    # Convert the list of dictionaries to a DataFrame for further processing if needed
    combined_df = pd.DataFrame(combined_list)

    # Convert the combined DataFrame to a list of dictionaries for rendering in the template
    data = combined_df.to_dict(orient="records")

    # Get the URL of the calling page, if available
    calling_page_url = request.args.get("calling_page")

    # Render the template with the combined data and calling page URL
    return render_template(
        "environments/environments_home.html",
        calling_page_url=calling_page_url,
        data=data,
    )

@api.doc(params={'data_product_id': 'The ID of the data product'})
@api.doc(params={'environment': 'The name of the environment'})
class EditEnvironment(Resource):
    @api.doc(description="Fetch and render the environment details for a given data product ID and environment.")
    @api.response(200, 'HTML Page rendered successfully')
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    def get(self, data_product_id, environment):

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("edit_environment"):
            try:
                logger.info("GET request")
                    
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                # Go up one directory from the current directory
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

                # Construct the path to the config directory based on data_product_id and environment
                config_directory_path = os.path.join(parent_dir, data_product_id, "config")

                file_name =  f"config.{environment}.json"
                # Construct the path to the specific JSON config file for the environment
                json_config_path = os.path.join(config_directory_path,file_name)
                
                logger.info(f"Looking for config file at: {json_config_path}")
                
                # Load the JSON config file
                if os.path.exists(json_config_path):
                    with open(json_config_path, 'r') as json_file:
                        config_data = json.load(json_file)
                else:
                    logger.error(f"Config file: {json_config_path} not found for {data_product_id} in environment {environment}")
                    config_data = {}  # Return an empty dictionary if the config file is missing

                # Get the URL of the calling page, if available
                calling_page_url = request.args.get("calling_page")

                # Render the template with the loaded config data
                return make_response(render_template(
                    "environments/edit_environment.html",
                    calling_page_url=calling_page_url,
                    data=config_data,  # Pass the config JSON data to the template
                    data_product_id=data_product_id,
                    environment=environment
                ))
            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    SERVICE_NAME, NAMESPACE_NAME, data_product_id, ENVIRONMENT
                ).error_with_exception(error_message, exc_info)
                return render_template("error.html", error_message=error_message)

    @api.doc(description="Update the environments config file with new data for a given data product and environment.")
    @api.response(200, 'Config file updated successfully')
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    def post(self, data_product_id, environment):

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("edit_environment"):
            try:
                logger.info("POST request")
                    
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                # Go up one directory from the current directory
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

                # Construct the path to the config directory based on data_product_id and environment
                config_directory_path = os.path.join(parent_dir, data_product_id, "config")

                file_name =  f"config.{environment}.json"
                # Construct the path to the specific JSON config file for the environment
                json_config_path = os.path.join(config_directory_path,file_name)

                logger.info(f"json_config_path:{json_config_path}")
                
                # Get the data from the request JSON
                new_config = request.json
                if not new_config:
                    return {"error": "No config provided"}, 400

                logger.info(f"Received new config data: {new_config}")

                # Save the updated DataFrame back to the CSV
                os.makedirs(config_directory_path, exist_ok=True)  # Ensure the directory exists
                with open(json_config_path, "w") as file:
                    json.dump(new_config, file, indent=2, sort_keys=False)
                logger.info(f"Config file updated successfully at {json_config_path}")

                return {"message": "Config file updated successfully"}, 200

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    SERVICE_NAME, NAMESPACE_NAME, data_product_id, ENVIRONMENT
                ).error_with_exception(error_message, exc_info)
                return render_template("error.html", error_message=error_message)

@api.doc(params={'data_product_id': 'The ID of the data product to query'})
class DatasetsList(Resource):
    @api.doc(description="Fetch and render the list of datasets for a given data product ID.")
    @api.response(200, 'HTML Page rendered successfully')
    @api.response(500, 'Internal Server Error')
    def get(self, data_product_id):
        """
        Retrieves and renders a list of datasets for a given data product ID.
        This function performs the following steps:
        1. Initializes logging and tracing.
        2. Constructs the path to a CSV file containing dataset configurations.
        3. Reads the CSV file into a pandas DataFrame.
        4. Converts the DataFrame to a list of dictionaries.
        5. Retrieves the calling page URL and available environments.
        6. Renders the datasets list template with the datasets and environments.
        Args:
            data_product_id (str): The ID of the data product for which datasets are to be listed.
        Returns:
            str: Rendered HTML template for the datasets list or an error page in case of an exception.
        Raises:
            Exception: If an unexpected error occurs during the process, an error page is rendered with the exception details.
        """
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("datasets_list"):
            try:

                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                # Go up one directory from the current directory
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

                # Construct the relative path to the CSV file
                csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
                csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_datasets.csv")
                logger.info(f"csv_path:{csv_path}")
                df = pd.read_csv(csv_path)
                # Convert the DataFrame to a list of dictionaries
                df = df.fillna(value='')  # You can replace `None` with another value, such as an empty string ''
                datasets = df.to_dict(orient="records")
    
                calling_page_url = request.url
                config_environments = list_config_environments(csv_directory_path)
                return make_response(render_template(
                    "datasets/datasets_list.html", calling_page_url=calling_page_url, datasets=datasets, environments=config_environments
                ))
            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    SERVICE_NAME, NAMESPACE_NAME, data_product_id, ENVIRONMENT
                ).error_with_exception(error_message, exc_info)
                return make_response(render_template("error.html", error_message=error_message))

    @api.doc(description="Update the datasets CSV file with new data for a given data product.")
    @api.response(200, 'CSV file updated successfully')
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    def post(self, data_product_id):
        """
        Update the datasets for the specified data product by modifying the CSV file on the server.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("datasets_list_post"):
            try:
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                if not data_product_id:
                    return {"error": "Missing 'data_product_id' in request"}, 400

                # Construct the relative path to the CSV file
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
                csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
                csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_datasets.csv")
                logger.info(f"csv_path:{csv_path}")

                # Expected columns in the DataFrame
                expected_columns = [
                    'data_product_id', 'database', 'dataset_name', 'file_name', 'folder_name', 'folder_name_source', 'format', 'row_id_keys', 'column_ordinal_sort', 
                    'dataset_friendly_name', 'dataset_description', 'crdy_domain', 'crdy_is_sa_dataset', 'crdy_maximum_latency_hours', 'crdy_subdomain', 'crdy_subdomain2', 
                    'edc_access_level', 'edc_alation_datasource_id', 'edc_alation_datasource_identifier', 'edc_alation_schema_id', 'edc_applicability_end_date', 
                    'edc_applicability_start_date', 'edc_citation', 'edc_conform_to_standard', 'edc_homepage_url', 'edc_identifier', 'edc_is_containing_pii', 'edc_language', 
                    'edc_license', 'edc_pii_comments', 'edc_pii_fields', 'edc_reference', 'edc_referenced_by', 'edc_release_date', 'edc_size', 'edc_submitting_user', 
                    'edc_tags', 'edc_update_frequency', 'encoding', 'entity', 'excluded_environments', 'frequency', 'incremental', 'is_active', 'is_export_schema_required', 
                    'is_multiline', 'is_refreshed', 'is_required_for_power_bi', 'optimize_columns', 'optimize_type', 'pii_columns', 'workflow_batch_group', 'data_product_id', 
                    'remove_columns_with_no_metadata', 'row_id_core_columns', 'use_liquid_clustering', 'partition_by', 'sheet_name', 'source_abbreviation', 
                    'source_dataset_name', 'source_json_path',
                ]

                logger.info(request.json)

                # Get the data from the request JSON
                new_datasets = request.json.get('data', [])
                if not new_datasets:
                    return {"error": "No datasets provided in 'data' array"}, 400

                logger.info(f"Received new dataset data: {new_datasets}")

                # Convert new_datasets list of dicts to a DataFrame
                new_datasets_df = pd.DataFrame(new_datasets)

                # Ensure new_datasets_df has the required columns, filling in missing columns with empty strings
                for column in expected_columns:
                    if column not in new_datasets_df.columns:
                        new_datasets_df[column] = ''

                # Save the updated DataFrame back to the CSV
                os.makedirs(csv_directory_path, exist_ok=True)  # Ensure the directory exists
                new_datasets_df.to_csv(csv_path, index=False)
                logger.info(f"CSV file updated successfully at {csv_path}")

                return {"message": "CSV file updated successfully"}, 200

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                
                # Log the error and return a 500 Internal Server Error
                logger.error(error_message, exc_info=True)
                return {"error": error_message}, 500

@api.doc(params={'data_product_id': 'The ID of the data product'})
@api.doc(params={'dataset_name': 'The name of the dataset'})
class DatasetsColumns(Resource):
    @api.doc(description="Fetch and render the list of datasets for a given data product ID.")
    @api.response(200, 'HTML Page rendered successfully')
    @api.response(500, 'Internal Server Error')
    def get(self, data_product_id, dataset_name):

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("datasets_list_columns"):
            try:
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                if not data_product_id:
                    return {"error": "Missing 'data_product_id' in request"}, 400

                # Construct the relative path to the CSV file
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
                csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
                csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_columns.csv")
                logger.info(f"csv_path:{csv_path}")

                column_df = pd.read_csv(csv_path)
                # Convert the DataFrame to a list of dictionaries
                column_df = column_df.fillna(value='')  # You can replace `None` with another value, such as an empty string ''
                filtered_column_df = column_df[column_df['dataset_name'] == dataset_name]
                columns = filtered_column_df.to_dict(orient="records")

                # Construct the relative path to the CSV file
                csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
                csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_datasets.csv")
                logger.info(f"csv_path:{csv_path}")
                datasets_df = pd.read_csv(csv_path)
                # Convert the DataFrame to a list of dictionaries
                datasets_df = datasets_df.fillna(value='')  # You can replace `None` with another value, such as an empty string ''
                # datasets = datasets_df.to_dict(orient="records")
                dataset_df = datasets_df.loc[datasets_df['dataset_name'] == dataset_name]
                dataset = dataset_df.to_dict(orient="records")
    
                calling_page_url = request.url
                config_environments = list_config_environments(csv_directory_path)
                return make_response(render_template(
                    "datasets/datasets_columns.html", calling_page_url=calling_page_url, columns=columns, dataset=dataset, environments=config_environments
                ))

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    SERVICE_NAME, NAMESPACE_NAME, data_product_id, ENVIRONMENT
                ).error_with_exception(error_message, exc_info)
                return make_response(render_template("error.html", error_message=error_message))

    @api.doc(description="Update the datasets columns CSV file with new data for a given dataset.")
    @api.response(200, 'CSV file updated successfully')
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    def post(self, data_product_id, dataset_name):
        """
        Update the dataset columns for the specified data product by modifying the CSV file on the server.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("datasets_list_columns"):
            try:
                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                if not data_product_id:
                    return {"error": "Missing 'data_product_id' in request"}, 400

                # Construct the relative path to the CSV file
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
                csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
                csv_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_columns.csv")
                logger.info(f"csv_path:{csv_path}")

                # Expected columns in the DataFrame
                expected_columns = [
                    '__meta_ingress_file_path','column_batch_group','column_group','column_name','column_label','column_description','compare_filter',
                    'compare_table','compare_row_id_keys','compare_row_columns','column_name_new','custom_function','database_name','dataset_name',
                    'date_format','function','data_product_id','expected_percent_null','expected_percent_to_not_be_null','expect_column_values_to_be_in_set',
                    'expect_column_values_to_not_be_in_set','apply_expectations_by_date','apply_expectations_for_n_dates_back',
                ]

                logger.info(request.json)

                # Get the data from the request JSON
                new_columns = request.json.get('data', [])
                if not new_columns:
                    return {"error": "No datasets provided in 'data' array"}, 400

                logger.info(f"Received new dataset data: {new_columns}")

                # Convert new_columns list of dicts to a DataFrame
                new_columns_df = pd.DataFrame(new_columns)

                # Ensure new_columns_df has the required columns, filling in missing columns with empty strings
                for column in expected_columns:
                    if column not in new_columns_df.columns:
                        new_columns_df[column] = ''

                # Save the updated DataFrame back to the CSV
                os.makedirs(csv_directory_path, exist_ok=True)  # Ensure the directory exists
                new_columns_df.to_csv(csv_path, index=False)
                logger.info(f"CSV file updated successfully at {csv_path}")

                return {"message": "CSV file updated successfully"}, 200

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                
                # Log the error and return a 500 Internal Server Error
                logger.error(error_message, exc_info=True)
                return {"error": error_message}, 500
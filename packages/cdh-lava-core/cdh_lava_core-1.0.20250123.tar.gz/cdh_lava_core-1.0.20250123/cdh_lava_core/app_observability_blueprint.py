import sys
import os
import traceback
from flask_restx import Resource, fields, reqparse, Api
from dotenv import load_dotenv
from flask import Blueprint, make_response, request, render_template
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
from cdh_lava_core.az_log_analytics_service.az_kql import AzKql

cdh_observability_bp = Blueprint('cdh_observabilty', __name__)

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
api = Api(cdh_observability_bp)  # Initialize Api with the blueprint
ENVIRONMENT = "dev"  # Set the environment name
DATA_PRODUCT_ID = "lava_core"

tracer, logger = LoggerSingleton.instance(
    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
).initialize_logging_and_tracing()

class DependencyGraph(Resource):
    """
    A Flask-RESTful resource that handles the retrieval and rendering of a dependency graph for AI operations.
        Resource (flask_restful.Resource): The base class for creating RESTful resources in Flask.
    Methods:
        get(operation_id: str, data_product_id: str, environment: str, page: int) -> flask.Response:
            Handles GET requests to retrieve and render the dependency graph for a specific AI operation.
                operation_id (str): The ID of the operation for which the dependency graph is to be retrieved.
                data_product_id (str): The ID of the data product associated with the operation.
                environment (str): The environment in which the operation is being executed (e.g., 'dev', 'prod').
                page (int): The page number for pagination of the dependency graph.
            Returns:
                flask.Response: An HTML response containing the rendered dependency graph or an error message.

    Args:
        Resource (_type_): _description_
    """
    def get(self, operation_id, data_product_id, environment, page):

        items_per_page = 10  # You can adjust this or make it configurable

        tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("dependency_graph"):
            try:
                logger.info(f"navigating to page: {page}")
                current_dir = os.path.dirname(__file__)

                dotenv_path = os.path.join(os.path.dirname(current_dir), "lava_core", ".env")
                if not os.path.exists(dotenv_path):
                    dotenv_path = os.path.join(os.path.dirname(current_dir), ".env")

                load_dotenv(dotenv_path)
                
                obj_az_kql = AzKql()
                chart_html = obj_az_kql.graph_ai_dependencies(operation_id, data_product_id, environment, page, items_per_page)
                calling_page_url = request.args.get("calling_page")


                html_content = render_template(
                    "observability/dependency_graph.html", 
                    calling_page_url=calling_page_url, 
                    chart=chart_html, 
                    operation_id=operation_id
                )
                response = make_response(html_content)
                response.headers['Content-Type'] = 'text/html'
                return response

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                html_content =  render_template("error.html", error_message=error_message)
                response = make_response(html_content)
                response.headers['Content-Type'] = 'text/html'
                return response


class JobStatusListData(Resource):
 
    def get(self,  data_product_id):

        items_per_page = 10  # You can adjust this or make it configurable
        page = 1
        tracer_singleton = TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        )

       
        with tracer.start_as_current_span("job_status_list_data"):
            try:
                logger.info(f"navigating to page: {page}")
                current_dir = os.path.dirname(__file__)

                dotenv_path = os.path.join(os.path.dirname(current_dir), "lava_core", ".env")
                if not os.path.exists(dotenv_path):
                    dotenv_path = os.path.join(os.path.dirname(current_dir), ".env")

                load_dotenv(dotenv_path)
                
                obj_az_kql = AzKql()
                job_list_data = obj_az_kql.query_job_status_list_for_data_product_id( data_product_id, ENVIRONMENT)
                 
                return job_list_data

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                html_content =  render_template("error.html", error_message=error_message)
                response = make_response(html_content)
                response.headers['Content-Type'] = 'text/html'
                return response

class JobStatusList(Resource):
 
    def get(self,  data_product_id):

        items_per_page = 10  # You can adjust this or make it configurable
        page = 1
        tracer_singleton = TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, ENVIRONMENT
        )
       
        with tracer.start_as_current_span("job_status_list"):
            try:
                logger.info(f"navigating to page: {page}")
                current_dir = os.path.dirname(__file__)

                dotenv_path = os.path.join(os.path.dirname(current_dir), "lava_core", ".env")
                if not os.path.exists(dotenv_path):
                    dotenv_path = os.path.join(os.path.dirname(current_dir), ".env")

                load_dotenv(dotenv_path)
                
                obj_az_kql = AzKql()
                job_list_data = obj_az_kql.query_job_status_list_for_data_product_id( data_product_id, ENVIRONMENT)
                calling_page_url = request.args.get("calling_page")

                tracer_singleton.force_flush()
                html_content = render_template(
                    "observability/job_list_status_home.html", 
                    calling_page_url=calling_page_url, 
                    data=job_list_data, 
                )
                response = make_response(html_content)
                response.headers['Content-Type'] = 'text/html'
                return response

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                html_content =  render_template("error.html", error_message=error_message)
                response = make_response(html_content)
                response.headers['Content-Type'] = 'text/html'
                return response

@cdh_observability_bp.route("/get_log_file_tail/<int:number_of_lines>")
def get_log_file_tail(number_of_lines):
    """
    Retrieves the tail of a log file and renders it in an HTML template.

    Args:
        number_of_lines (int): The number of lines to retrieve from the log file.

    Returns:
        str: The rendered HTML template containing the log file entries.

    Raises:
        Exception: If an internal server error occurs while fetching the log file.
        ValueError: If the log data is None, or if the number_of_lines is missing or blank.
    """

    tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
    ).initialize_logging_and_tracing()

    with tracer.start_as_current_span("get_log_file_tail"):
        try:
            log_data = None

            (
                status_code,
                number_of_lines,
                log_data,
            ) = LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
            ).get_log_file_tail(number_of_lines)
            if status_code == 500:
                error_msg = f"Internal Server Error fetching log file: The server encountered an error. {log_data}"
                raise Exception(error_msg)

            if log_data is None:
                raise ValueError(
                    f"Internal Server Error fetching log file: Log data is None. {log_data}"
                )

            if number_of_lines is None or number_of_lines == 0:
                raise ValueError(
                    "Internal Server Error fetching log file: number_of_lines is missing or blank"
                )

            log_entries = []

            for line_number, line in enumerate(log_data.strip().split("\n"), start=1):
                log_entries.append(line.split("\u001F"))

            for entry in log_entries:
                try:
                    asctime, name, module, lineno, levelname, message = entry
                    datetime_object = datetime.strptime(asctime, "%Y-%m-%d %H:%M:%S")
                    asctime = datetime_object.strftime("%Y-%m-%d %I:%M:%S %p")
                    entry = [asctime, name, module, lineno, levelname, message]
                except ValueError as ex:
                    logger.warning(f"Error parsing line: {str(ex)}")
                except IndexError:
                    logger.warning(f"Error: line has missing fields: {entry}")

            # Sort log_entries by date and time in descending order
            log_entries.sort(key=lambda entry: get_datetime(entry), reverse=True)

            return render_template("log_file.html", entries=log_entries)

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            exc_info = sys.exc_info()
            LoggerSingleton.instance(
                SERVICE_NAME, NAMESPACE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
            ).error_with_exception(error_message, exc_info)
            return render_template("error.html", error_message=error_message)


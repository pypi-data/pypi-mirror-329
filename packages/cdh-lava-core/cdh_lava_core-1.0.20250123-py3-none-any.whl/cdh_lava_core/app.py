"""
This module, app.py, serves as the primary entry point to the CDC Data Hub LAVA (CDH-LAVA) application.
"""

import sys
import os
import traceback
import subprocess
from datetime import datetime
import json
from flask import (
    request,
    render_template,
    Blueprint,
    jsonify,
    make_response,
    session,
    send_from_directory
)
from werkzeug.exceptions import HTTPException
from flask_restx import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask_cors import CORS
import pandas as pd
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry import metrics
from cdh_lava_core.app_security_blueprint import cdh_security_bp, azure_ad_authentication, AuthCallback, AzSubscriptionClientSecretVerification, ConnectApiKeyVerification, generate_code_verifier, ALLOWED_ORIGINS
from cdh_lava_core.app_orchestration_blueprint import cdh_orchestration_bp, DataProductsData, JobRun,  DataProductsForJobs, DataProductsForQueries, DataProductsForDatasets, QueriesList, data_product_model, queries_model, query_model, list_config_environments, DatasetsList, DatasetsColumns, EditEnvironment
from cdh_lava_core.app_configuration_blueprint import cdh_configuration_bp, MetadataExcelFileUploadCodes
from cdh_lava_core.app_startup_blueprint import create_api, create_app
from cdh_lava_core.app_observability_blueprint import cdh_observability_bp, DependencyGraph, JobStatusList, JobStatusListData
from cdh_lava_core.app_great_expectations_blueprint import great_expectations_bp, GreatExpectationsHomeList, GreatExpectationHome, GreatExpectationModule, GreatExpectationPage
from cdh_lava_core.app_altmetric_blueprint import AltmetricDownload
from cdh_lava_core.app_shared_dependencies import get_config
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import cdh_lava_core.app_shared_dependencies as shared

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))

# Define hardcoded credentials for local development
HARD_CODED_USER = "Test User"
HARD_CODED_USER_ID = "test@cdc.gov"
USE_HARDCODED_LOGIN = os.getenv("USE_HARDCODED_LOGIN", "false").lower() == "true"

DATA_PRODUCT_ID = "lava_core"
TIMEOUT_5_SEC = 5
TIMEOUT_ONE_MIN = 60
# Get the currently running file name
ENVIRONMENT = "dev"

print(f"SERVICE_NAME:{SERVICE_NAME}")
print(f"NAMESPACE_NAME: {NAMESPACE_NAME}")
sys.path.append(os.getcwd())
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_dir)

app = create_app()
# handle posit flask gateway
if 'RS_SERVER_URL' in os.environ and os.environ['RS_SERVER_URL']:
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1, x_proto=1, x_host=1)

app.config['SECRET_KEY'] = '46837a7315f2306ada8f593bea518c75'

@app.route("/static/docs-cdc-datahub/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

tracer, logger = LoggerSingleton.instance(
    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
).initialize_logging_and_tracing()


# handle posit flask gateway
@app.before_request
def before_request():
    """
    A function to be executed before each request to handle specific request modifications and user session management.
    This function performs the following tasks:
    1. Exempts CSRF protection for requests containing "callback" in their path.
    2. If `USE_HARDCODED_LOGIN` is enabled:
        - Sets the user session to hardcoded credentials.
        - Logs the usage of hardcoded user credentials.
    3. If `USE_HARDCODED_LOGIN` is not enabled:
        - Sets the user session based on the existing session data.
        - Logs the request scheme.
        - Forces the URL scheme to HTTPS if the 'X-RStudio-Proto' header is set to 'https' and modifies the session to ensure secure cookies.
    Note:
    - `request` and `session` are assumed to be part of the Flask context.
    - `logger` is assumed to be a configured logging instance.
    - `USE_HARDCODED_LOGIN`, `HARD_CODED_USER_ID`, and `HARD_CODED_USER` are assumed to be predefined constants.
    """


    if "callback" in request.path:
        setattr(request, "_csrf_exempt", True)

    if USE_HARDCODED_LOGIN:
        # Use hardcoded credentials when running locally or in Posit Workbench
        session['user_id'] = HARD_CODED_USER_ID
        request.user = HARD_CODED_USER
        print(f"Using hardcoded user: {HARD_CODED_USER}")
        if 'user_id' in session:
            request.user = session['user_id']
        else:
            request.user = None
        logger.info("HARDCODED_ROUTE")
    else:
        if 'user_id' in session:
            request.user = session['user_id']
        else:
            request.user = None

        # logger.info('Headers: %s', request.headers)
        logger.info('Scheme: %s', request.scheme)

        if request.headers.get('X-RStudio-Proto') == 'https':
            request.environ['wsgi.url_scheme'] = 'https'
            session.modified = True  # Force secure cookie

# Apply CORS
config = app.cdc_config
lava_cors_url_list = config["lava_cors_url_list"]
url_array = lava_cors_url_list.strip("'").split(",")
logger.info(f"cors url list: {str(url_array)}")
CORS(
    app,
    origins=ALLOWED_ORIGINS,
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials",
    ],
    resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}},
    supports_credentials=True,
)


# Define the blueprint
cdc_admin_bp = Blueprint("logs", __name__, url_prefix="/logs")
cdc_files_bp = Blueprint("files", __name__, url_prefix="/files")
cdc_api_bp = Blueprint("api", __name__, url_prefix="/api")
cdc_modules_bp = Blueprint("modules", __name__, url_prefix="/modules")
cdc_environments_bp = Blueprint("environments", __name__, url_prefix="/environments")
cdc_queries_bp = Blueprint("queries", __name__, url_prefix="/queries")
cdc_datasets_bp = Blueprint("datasets", __name__, url_prefix="/datasets")
cdc_users_bp = Blueprint("users", __name__, url_prefix="/users")
cdc_files_protected_bp = Blueprint("protected_files", __name__, url_prefix="/protected_files")
altmetric_bp = Blueprint("altmetric", __name__, url_prefix="/altmetric")


@app.route("/synthea/")
def home():
    return render_template("synthea/synthea_home.html")

@app.route("/synthea/generate")
def generate():
    # Assuming you have a DataFrame with Synthea module names
    df_synthea_modules = pd.DataFrame({
        'synthea_module_names': ['Module1', 'Module2', 'Module3', 'Module4']
    })
    synthea_module_names = df_synthea_modules['synthea_module_names'].tolist()
    return render_template("synthea/synthea_generate.html", synthea_module_names=synthea_module_names)

@app.route("/synthea/visualize")
def visualize():
    return render_template("synthea/synthea_visualize.html")

@app.route("/synthea/generate", methods=["POST"])
def generate_data():
    data = request.get_json()
    patient_count = data.get("patientCount")
    # Assuming Synthea is set up to be called via a subprocess
    result = subprocess.run(["./run_synthea", "-p", patient_count], capture_output=True, check=True)
    if result.returncode == 0:
        return jsonify(count=patient_count)
    else:
        return jsonify(error="Failed to generate data"), 500

@app.route("/")
def index():
    return render_template("index.html")



@cdc_files_bp.route("/reports")
def reports():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file
    csv_path = os.path.join(parent_dir, "lava_core", "bronze_reports.csv")

    df = pd.read_csv(csv_path)
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    calling_page_url = request.args.get("calling_page")
    return render_template(
        "reports/reports_home.html", calling_page_url=calling_page_url, data=data
    )


@cdc_files_bp.route("/dashboards")
def dashboards():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file
    csv_path = os.path.join(parent_dir, "lava_core", "bronze_dashboards.csv")

    df = pd.read_csv(csv_path)
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    calling_page_url = request.args.get("calling_page")
    return render_template(
        "dashboards/dashboards_home.html", calling_page_url=calling_page_url, data=data
    )

@cdc_modules_bp.route("/module/<module_name>")
def module(module_name):
    data = {}
    # Implement the logic to display the module based on the module_name
    calling_page_url = request.args.get("calling_page")
    module_name = module_name.lower()
    return render_template(
        f"{module_name}/{module_name}_home.html",
        calling_page_url=calling_page_url,
        data=data,
    )


@cdc_modules_bp.route("/modules")
def modules():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file
    csv_path = os.path.join(parent_dir, "lava_core", "bronze_modules.csv")

    df = pd.read_csv(csv_path)
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    calling_page_url = request.args.get("calling_page")
    return render_template(
        "modules/modules_home.html", data=data, calling_page_url=calling_page_url
    )


@cdc_users_bp.route("users")
def users():
    """
    Fetches user data from a CSV file and renders the users' home page.
    This function performs the following steps:
    1. Determines the directory of the current file.
    2. Navigates up one directory from the current directory.
    3. Constructs the relative path to the 'bronze_users.csv' file located in the 'lava_core' directory.
    4. Reads the CSV file into a pandas DataFrame.
    5. Converts the DataFrame to a list of dictionaries.
    6. Retrieves the 'calling_page' URL parameter from the request arguments.
    7. Renders the 'users_home.html' template with the user data and the calling page URL.
    Returns:
        A rendered HTML template for the users' home page with user data and the calling page URL.
    """
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file
    csv_path = os.path.join(parent_dir, "lava_core", "bronze_users.csv")

    df = pd.read_csv(csv_path)
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    calling_page_url = request.args.get("calling_page")
    return render_template(
        "users/users_home.html",
        calling_page_url=calling_page_url,
        data=data,
    )

@cdc_admin_bp.route("/error")
def error():
    error_message = "An unexpected error occurred"
    return render_template("error.html", error_message=error_message, error_url="")

FlaskInstrumentor().instrument_app(app)

if ENVIRONMENT == "prod":
    INSTRUMENTATION_KEY = "e7808e07-4242-4ed3-908e-c0a4c3b719b1"
else:
    INSTRUMENTATION_KEY = "8f02ef9a-cd94-48cf-895a-367f102e8a24"

if INSTRUMENTATION_KEY is None:
    raise ValueError("APPLICATIONINSIGHTS_INSTRUMENTATION_KEY environment variable is not set")

# Set up metrics exporter (optional)
metrics_exporter = AzureMonitorMetricExporter(
    connection_string=f"InstrumentationKey={INSTRUMENTATION_KEY}"
)
# Set up the metric reader and provider
metric_reader = PeriodicExportingMetricReader(metrics_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader])

# Set the meter provider globally
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Create a counter for availability monitoring
availability_counter = meter.create_counter(
    name="website_availability",
    unit="1",
    description="Counts availability checks for the website"
)

API_DESCRIPTION = """
<h2>API Documentation</h2>
<p>CDC Data Hub LAVA (CDH) provides shared resources,
practices and guardrails for analysts to discover, access, link, and use
agency data in a consistent way. CDH improvements in standardized and 
streamlined workflows reduce the effort required to find, access, and
trust data.</p>
<p><a href="./">Back to Home</a></p>
<p><a href="./cdh_configuration/upload_codes?data_product_id=premier_respiratory">Config Upload Page</a></p>
<p><a href="./protected_files/upload_edc">EDC Upload Page</a></p>
<p><a href="./files/download_edc">EDC Download Page</a></p>
<p>For detailed logs, please visit the <a href="../logs/get_log_file_tail/1000">Log File Page</a>.</p>
"""
api = None

(
    api,
    ns_welcome,
    ns_alation,
    ns_jira,
    ns_posit,
    ns_cdc_admin,
    ns_cdh_security,
    ns_altmetric,
    ns_cdh_orchestration,
    ns_cdh_configuration,
    ns_cdh_observability,
    ns_great_expectations
) = create_api(app, API_DESCRIPTION)

# General error handler for other exceptions to return JSON
@app.errorhandler(Exception)
def handle_generic_error(e):
    if isinstance(e, HTTPException):
        # If it's a built-in HTTP error, return the default message
        return jsonify(error=e.name, description=e.description), e.code
    else:
        # For any other exceptions, return a custom message
        return jsonify(error="Internal Server Error", message=str(e)), 500

 
class WelcomeSwaggerJson(Resource):
    def get(self):
        """
        Returns the Swagger API documentation.

        Returns:
            dict: The Swagger API documentation schema.
        """
        
        return api.__schema__


class WelcomeSwagger(Resource):
    def get(self):
        """
        Returns the Swagger API documentation.

        Returns:
            Response: Rendered Swagger UI page.
        """
        
        # Render the Swagger UI template and return as response
        return make_response(render_template("swagger_ui.html"))


# Define the API description with a hyperlink to the log file page
api.description = API_DESCRIPTION
# Add the WelcomeSwagger resource to the Api instance
api.add_resource(WelcomeSwagger, "/swagger")
api.add_resource(WelcomeSwaggerJson, "/swagger/swagger.json")
# Register the model with the namespace if not already done
api.models[data_product_model.name] = data_product_model
api.models[queries_model.name] = queries_model
api.models[query_model.name] = query_model


ns_cdh_configuration.add_resource(MetadataExcelFileUploadCodes, '/upload_codes/<string:data_product_id>')

ns_cdh_security.add_resource(AuthCallback, '/callback')
ns_cdh_security.add_resource(AzSubscriptionClientSecretVerification, '/azsubscriptionclientsecretverification')
ns_cdh_security.add_resource(ConnectApiKeyVerification, '/connectapikeyverification')

ns_cdh_orchestration.add_resource(JobRun, "/job_run")
ns_cdh_orchestration.add_resource(DataProductsForJobs, "/data_products_for_jobs")
ns_cdh_orchestration.add_resource(DataProductsForQueries, "/data_products_for_queries")
ns_cdh_orchestration.add_resource(DataProductsForDatasets, "/data_products_for_datasets")
ns_cdh_orchestration.add_resource(DataProductsData, "/data_products_data")
ns_cdh_orchestration.add_resource(QueriesList, "/queries_list/<string:data_product_id>")
ns_cdh_orchestration.add_resource(QueriesList, "/queries_list/<string:data_product_id>")

ns_cdh_orchestration.add_resource(DatasetsList, "/datasets_list/<data_product_id>")
ns_cdh_orchestration.add_resource(DatasetsColumns, "/datasets_list/<data_product_id>/datasets_column/<string:dataset_name>")
ns_cdh_orchestration.add_resource(EditEnvironment, "/edit_environment/<data_product_id>/environment/<environment>")

ns_cdh_observability.add_resource(DependencyGraph, "/dependency_graph/<string:operation_id>/<string:data_product_id>/<string:environment>/<int:page>")
ns_cdh_observability.add_resource(JobStatusList, "/job_status_list/<string:data_product_id>")
ns_cdh_observability.add_resource(JobStatusListData, "/job_status_list_data/<string:data_product_id>")

ns_great_expectations.add_resource(GreatExpectationsHomeList, "great_expectations_list")
ns_great_expectations.add_resource(GreatExpectationHome, "/great_expectation/<string:data_product_id>/<string:text>")
ns_great_expectations.add_resource(GreatExpectationModule, "/great_expectation/<string:data_product_id>/<string:module>/<string:text>")
ns_great_expectations.add_resource(GreatExpectationPage,  "/great_expectation/<string:data_product_id>/<string:module>/<string:suite>/<string:run>/<string:page>/<string:text>")

ns_altmetric.add_resource(AltmetricDownload, "/altmetric_download/download_altmetric_data/<string:altmetric_id>")
app.register_blueprint(cdh_security_bp)
app.register_blueprint(cdh_orchestration_bp)
app.register_blueprint(cdh_configuration_bp)
app.register_blueprint(cdh_observability_bp)
app.register_blueprint(cdc_api_bp)
app.register_blueprint(cdc_admin_bp)
app.register_blueprint(cdc_files_bp)
app.register_blueprint(cdc_files_protected_bp)
app.register_blueprint(cdc_modules_bp)
app.register_blueprint(cdc_users_bp)
app.register_blueprint(cdc_environments_bp)
app.register_blueprint(great_expectations_bp)
app.register_blueprint(altmetric_bp)

metric_exporter = AzureMonitorMetricExporter()

if __name__ == "__main__":
    app.run(debug=True)
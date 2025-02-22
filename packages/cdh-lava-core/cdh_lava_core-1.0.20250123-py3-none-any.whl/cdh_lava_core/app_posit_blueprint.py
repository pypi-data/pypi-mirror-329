import sys
import os
from flask_restx import Resource, fields, reqparse
from cdh_lava_core.posit_service import (
    posit_connect as cdh_posit_connect,
)
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))


class DeploymentBundle(Resource):
    """
    A Flask-RESTful resource for handling POSIT Deployment Bundle.

    """

    def get(self, content_id, bundle_id):
        """
        Generates DeploymentBundle

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span("build_deployment_bundle"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key"
            )
            connect_api_key = app_security.get_posit_api_key()
            posit_connect = cdh_posit_connect.PositConnect()
            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.build_deployment_bundle(
                connect_api_key,
                posit_connect_base_url,
                content_id,
                bundle_id,
                DATA_PRODUCT_ID,
                ENVIRONMENT,
            )

            # Handle the verification logic
            return {
                "posit_connect_base_url": posit_connect_base_url,
                "api_url": api_url,
                "response_content": response_content,
            }

class PythonInformation(Resource):
    """
    A Flask-RESTful resource for handling POSIT Python Information.

    """
    
    def get(self):
        """
        Generates python information about POSIT

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"api_key_verification"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key"
            )
            connect_api_key = get_posit_api_key()
            posit_connect = cdh_posit_connect.PositConnect()
            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.get_python_information(
                connect_api_key, posit_connect_base_url
            )

            # Handle the verification logic
            return {
                "posit_connect_base_url": posit_connect_base_url,
                "api_url": api_url,
                "az_kv_posit_connect_secret_key": az_kv_posit_connect_secret_key,
                "response_content": response_content,
            }



class GeneratedManifestJson(Resource):
    """
    A Flask-RESTful resource for handling POSIT ManifestJson Generation

    """

    def get(self):
        """
        Generates manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"generate_manifest"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            # Get the full URL
            full_url = request.url
            # Split the URL by '/'
            url_parts = full_url.split("/")
            # Remove the last 2 parts (i.e., the file name or the route)
            url_parts = url_parts[:-2]
            # Join the parts back together
            url_without_filename = "/".join(url_parts)
            base_url = url_without_filename
            environment = config.get("environment")
            obj_file = cdc_env_file.EnvironmentFile()

            app_dir = os.path.dirname(os.path.abspath(__file__))

            manifest_path = app_dir + "/" + environment + "_posit_manifests/"

            swagger_path = app_dir + "/" + environment + "_swagger_manifests/"

            yyyy = str(datetime.now().year)
            dd = str(datetime.now().day).zfill(2)
            mm = str(datetime.now().month).zfill(2)

            json_extension = "_" + yyyy + "_" + mm + "_" + dd + ".json"
            manifest_json_file = manifest_path + "manifest" + json_extension
            # swagger_file = swagger_path + "swagger" + json_extension
            # use cached json file for now
            # having issues downloading
            swagger_file = swagger_path + "swagger_2023_06_22.json"
            connect_api_key = get_posit_api_key()
            requirements_file = app_dir + "/requirements.txt"

            # headers = {
            #     "Authorization": f"Bearer {connect_api_key}",
            # }
            swagger_url = f"{base_url}/swagger.json"
            # response = requests.get(swagger_url, headers=headers)

            # response_data = None
            # error_message = None
            # if response.status_code == 200:  # HTTP status code 200 means "OK"
            #     try:
            #         response_data =  response.json()
            #         response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            #   except requests.HTTPError as http_err:
            #        error_message = f"HTTP error occurred: {http_err}"
            #        soup = BeautifulSoup(response.text, 'html.parser')
            #        error_message = (soup.prettify())
            #    except JSONDecodeError:
            #        error_message = "The response could not be decoded as JSON."
            #        soup = BeautifulSoup(response.text, 'html.parser')
            #        error_message = (soup.prettify())
            #    except Exception as err:
            #        error_message = f"An error occurred: {err}"
            #        error_message = "Response content:"+ response.content.decode()
            # else:
            #    error_message = f"Request failed with status code {response.status_code}"
            # if error_message is not None:
            #    return {
            #        'headers' : headers,
            #        'swagger_url' :  swagger_url,
            #        'manifest_json': "",
            #        'status_message': error_message
            #    }, 500
            # with open(swagger_file, 'w') as f:
            #    f.write(response_data)

            logger.info(f"swagger_file:{swagger_file}")

            posit_connect = cdh_posit_connect.PositConnect()

            manifest_json = posit_connect.generate_manifest(
                swagger_file, requirements_file
            )

            with open(manifest_json_file, "w") as f:
                f.write(manifest_json)

            # Handle the verification logic
            return {
                "swagger_url": swagger_url,
                "manifest_json": manifest_json,
                "status_message": "success",
            }

 

class PublishManifestJson(Resource):
    """
    A Flask-RESTful resource for handling POSIT ManifestJsonJson Publication

    """

    def get(self):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"publish_manifest"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            # Get the full URL
            full_url = request.url
            # Split the URL by '/'
            url_parts = full_url.split("/")
            # Remove the last 2 parts (i.e., the file name or the route)
            url_parts = url_parts[:-2]
            # Join the parts back together
            url_without_filename = "/".join(url_parts)
            base_url = url_without_filename
            environment = config.get("environment")
            obj_file = cdc_env_file.EnvironmentFile()

            app_dir = os.path.dirname(os.path.abspath(__file__))

            manifest_path = app_dir + "/" + environment + "_posit_manifests/"

            manifest_json_file = obj_file.get_latest_file(manifest_path, "json")

            logger.info(f"manfiest_file:{manifest_json_file}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key"
            )
            connect_api_key = get_posit_api_key()

            posit_connect = cdh_posit_connect.PositConnect()

            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.publish_manifest(
                connect_api_key, posit_connect_base_url, manifest_json_file
            )

            # Handle the verification logic
            return {
                "status_code": status_code,
                "response_content": response_content,
                "api_url": api_url,
            }


class ContentList(Resource):
    """
    A Flask-RESTful resource for handling POSIT Content Lists

    """

    def get(self):
        """
        Retrieves the manifest JSON for the content list.

        Returns:
            tuple: A tuple containing the status code and response from the server.
                   The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span("list_content"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            connect_api_key = get_posit_api_key()

            posit_connect = cdh_posit_connect.PositConnect()

            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.list_content(connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                "status_code": status_code,
                "response_content": response_content,
                "api_url": api_url,
            }


class DeploymentBundleList(Resource):
    """
    A Flask-RESTful resource for handling POSIT Bundle Lists

    """

    def get(self, content_id):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span("list_deployment_bundles"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key"
            )
            connect_api_key = get_posit_api_key()

            posit_connect = cdh_posit_connect.PositConnect()

            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.list_deployment_bundles(
                connect_api_key, posit_connect_base_url, content_id
            )

            # Handle the verification logic
            return {
                "status_code": status_code,
                "response_content": response_content,
                "api_url": api_url,
            }


class TaskStatus(Resource):
    """
    A Flask-RESTful resource for handling POSIT Bundle Lists

    """

    def get(self, task_id):
        """
        Gets Task Status

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"get_task_status"):
            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key"
            )
            connect_api_key = get_posit_api_key()

            posit_connect = cdh_posit_connect.PositConnect()

            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.get_task_details(
                connect_api_key, posit_connect_base_url, task_id
            )

            # Handle the verification logic
            return {
                "status_code": status_code,
                "response_content": response_content,
                "api_url": api_url,
            }



ns_posit.add_resource(ConnectApiKeyVerification, "/connect_api_key_verification")
ns_posit.add_resource(PythonInformation, "/python_information")
ns_posit.add_resource(GeneratedManifestJson, "/generate_manifest")
ns_posit.add_resource(PublishManifestJson, "/publish_manifest")
ns_posit.add_resource(ContentList, "/list_content")
ns_posit.add_resource(
    DeploymentBundle,
    "/build_deployment_bundle/<string:content_id>/<string:bundle_id>",
)
ns_posit.add_resource(
    DeploymentBundleList, "/list_deployment_bundles/<string:content_id>"
)
ns_posit.add_resource(TaskStatus, "/get_task_status/<string:task_id>")

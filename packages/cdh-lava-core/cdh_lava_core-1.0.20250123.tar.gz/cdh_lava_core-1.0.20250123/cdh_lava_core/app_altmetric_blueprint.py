import sys
import os
import json
from flask import Blueprint, render_template_string, jsonify
from flask import render_template, request, make_response
from flask_restx import Resource, fields, reqparse
import traceback
from cdh_lava_core.altmetric_service.altmetric_downloader import AltmetricDownloader
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
from cdh_lava_core.app_shared_dependencies import get_config

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))

parser = reqparse.RequestParser()
parser.add_argument("environment", location="form", type=str, required=True)
parser.add_argument("data_product_id", location="form", type=str, required=True)


class AltmetricDownload(Resource):
    """
    Represents a resource for downloading Altmetric data.
    """

    def get(self, altmetric_id=None):
        """
        Handles the GET request for downloading Altmetric data.

        Parameters:
            altmetric_id: Altmetric number used to retrieve document metadata. (Example: 149664243)

        Returns:
            A JSON response containing the downloaded Altmetric data, or an error message if the download_edc fails.
        """

        master_config = get_config()

        data_product_id = master_config.get("data_product_id")
        environment = master_config.get("environment")
       
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("__init__"):
            try:
                if not altmetric_id:
                    return jsonify({"error": "altmetric_id parameter is required"}), 400

                if not data_product_id:
                    return (
                        jsonify({"error": "data_product_id parameter is required"}),
                        400,
                    )

                obj_altmetric_downloader = AltmetricDownloader()
                results = obj_altmetric_downloader.download_altmetric_data(
                    altmetric_id, data_product_id, environment
                )

                if results is None:
                    return (
                        jsonify({"error": "Failed to download_edc Altmetric data"}),
                        500,
                    )

                return jsonify(results)

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                exc_info = sys.exc_info()
                # logger_singleton.error_with_exception(error_message, exc_info)
                return render_template("error.html", error_message=error_message)

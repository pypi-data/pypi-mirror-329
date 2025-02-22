""" Module for rep_core for it_cdc_admin_service that handles repository and cluster functions with minimal dependencies. """

import os
import sys
import json
from html.parser import HTMLParser  # web scraping html
import requests

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class DbxCluster:
   

    @classmethod
    def create_serverless_job_cluster(cls, config, token, data_product_id, environment,  cluster_name="serverless-job-cluster", spark_version="14.3.x-photon-scala2.12", node_type_id="Standard_D3_v2", min_workers=1, max_workers=3, autotermination_minutes=20):

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()
        
        with tracer.start_as_current_span("create_serverless_job_cluster"):
            try:
        
                cdh_databricks_instance_id = config.get("cdh_databricks_instance_id")
                databricks_instance = f"https://{cdh_databricks_instance_id}"
                
                url = f"{databricks_instance}/api/2.0/clusters/create"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                cluster_config = {
                    "cluster_name": cluster_name,
                    "spark_version": spark_version,
                    "node_type_id": node_type_id,
                    "enable_photon": True,
                    "autoscale": {
                        "min_workers": min_workers,
                        "max_workers": max_workers
                    },
                    "autotermination_minutes": autotermination_minutes,
                    "spark_conf": {
                        "spark.databricks.cluster.profile": "serverless",
                        "spark.databricks.repl.allowedLanguages": "python,sql"
                    },
                    "custom_tags": {
                        "usage": "serverless-job"
                    },
                    "spark_env_vars": {
                        "PYSPARK_PYTHON": "/databricks/python3/bin/python3"
                    }
                }

                response = requests.post(url, headers=headers, data=json.dumps(cluster_config))

                if response.status_code == 200:
                    print("Cluster created successfully!")
                    return response.json()
                else:
                    error_msg = f"Failed to create cluster: {response.status_code}"
                    error_msg = error_msg + response.text
                    raise ValueError(error_msg)
                    return None

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
 
class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


class CDHObject(object):
    pass

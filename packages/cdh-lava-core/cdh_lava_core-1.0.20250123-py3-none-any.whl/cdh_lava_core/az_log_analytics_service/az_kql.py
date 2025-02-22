
from cdh_lava_core.az_key_vault_service.az_key_vault import AzKeyVault
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
import os
import sys
import requests
from datetime import datetime

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
APPLICATIONINSIGHTS_APPLICATION_ID_PROD="b05ee49c-b741-4d66-bb02-9ecd727d8361"
APPLICATIONINSIGHTS_API_KEY_PROD="a7ymbqkn2ooxegnynfgrpe2fqkjx1c6to13shul6"
APPLICATIONINSIGHTS_APPLICATION_ID_DEV="48a71f9c-8c54-4a73-ada1-36e87c6e7347"
APPLICATIONINSIGHTS_API_KEY_DEV="nzhoap6jtnqn50efr0p7xnsgcatz0palrjib8swe"
class AzKql:
    """
    A class that provides utility methods for working with files in Azure Data Lake Storage.
    """

    @classmethod
    def format_duration_from_ms(cls, duration_in_ms):
        if duration_in_ms >= 1000:
            return f"{duration_in_ms / 1000:.2f} s"
        else:
            return f"{duration_in_ms} ms"

    @classmethod
    def format_duration(cls, duration_in_seconds):
        """
        Dynamically format the duration: display in minutes if it's more than 60 seconds.
        """
        if duration_in_seconds >= 60:
            minutes = duration_in_seconds / 60
            return f"{minutes:.2f} minutes"
        else:
            return f"{duration_in_seconds:.2f} seconds"


    def get_application_name_from_api_key(self, config, data_product_id, environment):
        """
        Fetches the Application Name from Azure Application Insights using the Instrumentation Key.

        Returns:
            str: The Application Name.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_application_name_from_api_key"):
            try:
                return "unable_to_get_app_insights_name"

                client_secret = os.environ.get("AZURE_CLIENT_SECRET")
                if client_secret is None:
                    client_secret = config.get("client_secret")
                az_sub_client_secret_key = config.get("az_sub_client_secret_key")
                if client_secret is None:
                    az_sub_client_secret_key_env = az_sub_client_secret_key.replace("-", "_")
                    az_sub_client_secret_key_env = az_sub_client_secret_key_env.upper()
                    client_secret = os.getenv(az_sub_client_secret_key_env)
                if client_secret is None:
                    return "unable_to_get_app_insights_name"
                tenant_id = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_client_id")
                vault_name = config.get("az_kv_key_vault_name")
                data_product_id = config.get("data_product_id")
                environment = config.get("environment")
                running_local = not (("dbutils" in locals() or "dbutils" in globals()) and dbutils is not None)
                if running_local:
                    running_interactive = True
                else:
                    running_interactive = False
                    
                obj_key_vault = AzKeyVault(
                    tenant_id,
                    client_id,
                    client_secret,
                    vault_name,
                    running_interactive,
                    data_product_id,
                    environment,
                    az_sub_client_secret_key
                )
                
                if environment == "prod":
                    url = f"https://api.applicationinsights.io/v1/apps/{APPLICATIONINSIGHTS_APPLICATION_ID_PROD}/metadata"

                    # Headers
                    headers = {
                        "X-Api-Key": APPLICATIONINSIGHTS_API_KEY_PROD,
                        "Content-Type": "application/json"
                    }
                else:
                    url = f"https://api.applicationinsights.io/v1/apps/{APPLICATIONINSIGHTS_APPLICATION_ID_DEV}/metadata"

                    # Headers
                    headers = {
                        "X-Api-Key": APPLICATIONINSIGHTS_API_KEY_DEV,
                        "Content-Type": "application/json"
                    }

                # Make the request
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes

                data = response.json()
                if 'applications' in data and data['applications']:
                    return data['applications'][0]['name']
                elif 'name' in data:
                    return data['name']
                else:
                    raise ValueError("Application name not found in the response.")

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    def get_access_token(self):
        """
        Fetches an Azure access token using the Azure Instance Metadata Service (IMDS).

        Returns:
            str: The access token.
        """
        try:
            # Request an access token from the Azure Instance Metadata Service (IMDS)
            url = "http://169.254.169.254/metadata/identity/oauth2/token"
            params = {
                "api-version": "2018-02-01",
                "resource": "https://management.azure.com/"
            }
            headers = {"Metadata": "true"}
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                logging.error(f"Failed to retrieve access token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving access token: {str(e)}")
            return None
                    
    @classmethod
    def graph_ai_dependencies(cls, operation_id, data_product_id, environment, page, items_per_page=10):
        if environment == "prod":
            app_id = APPLICATIONINSIGHTS_APPLICATION_ID_PROD
            api_key = APPLICATIONINSIGHTS_API_KEY_PROD
        else:
            app_id = APPLICATIONINSIGHTS_APPLICATION_ID_DEV
            api_key = APPLICATIONINSIGHTS_API_KEY_DEV

        from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("graph_ai_dependencies"):
            try:
                all_data = cls.query_ai_dependencies_by_operation_id(operation_id, data_product_id, environment)

                if not all_data:
                    return "No data available"

                timestamps = [datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ') for row in all_data]
                start_time = min(timestamps)
                end_time = max(timestamps)
                overall_duration_in_seconds = (end_time - start_time).total_seconds()

                formatted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_overall_duration = cls.format_duration(overall_duration_in_seconds)

                summary_table_html = f'''
                <h2>Dependency Timeline Summary</h2> <br/>for Operation ID: {operation_id}
                <br/>for Data Product Id: {data_product_id}, Environment: {environment} <br/>
                <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                    <thead style="background-color: #f2f2f2;">
                        <tr>
                            <th>Start Time</th>
                            <th>End Time</th>
                            <th>Overall Duration</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{formatted_start_time}</td>
                            <td>{formatted_end_time}</td>
                            <td>{formatted_overall_duration}</td>
                        </tr>
                    </tbody>
                </table>
                '''

                unique_data = []
                previous_row = None
                for row in all_data:
                    if previous_row is None or row[1:] != previous_row[1:]:
                        unique_data.append(row)
                    previous_row = row

                total_items = len(unique_data)
                items_per_page = int(items_per_page)
                total_pages = (total_items + items_per_page - 1) // items_per_page

                page = max(1, min(page, total_pages))

                start_index = (page - 1) * items_per_page
                end_index = start_index + items_per_page
                paged_data = unique_data[start_index:end_index]

                table_html = f'''
                <h2>Dependency Details (Page {page} of {total_pages})</h2>
                <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                    <thead style="background-color: #f2f2f2;">
                        <tr>
                            <th>Name</th>
                            <th>Duration</th>
                            <th>Success</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

                for i, row in enumerate(paged_data):
                    name = row[1]
                    duration = cls.format_duration_from_ms(row[3] / 1000)
                    success = 'Success' if row[4] else 'Failure'

                    row_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
                    success_color = "green" if success == "Success" else "red"

                    table_html += f'''
                    <tr style="background-color: {row_color};">
                        <td>{name}</td>
                        <td>{duration}</td>
                        <td style="color: {success_color}; font-weight: bold;">{success}</td>
                    </tr>
                    '''

                table_html += '''
                    </tbody>
                </table>
                '''
                                
                pagination_html = f'''
                    <div style="margin-top: 20px; text-align: center;">
                        <span>Page {page} of {total_pages}</span>
                        <br>
                        {'<a href="#" onclick="changePage(1)">First</a> ' if page > 1 else ''}
                        {'<a href="#" onclick="changePage(' + str(page-1) + ')">Previous</a> ' if page > 1 else ''}
                        {'<a href="#" onclick="changePage(' + str(page+1) + ')">Next</a> ' if page < total_pages else ''}
                        {'<a href="#" onclick="changePage(' + str(total_pages) + ')">Last</a>' if page < total_pages else ''}
                    </div>
                    <script>
                    function changePage(newPage) {{
                        // Get the current pathname
                        var currentPath = window.location.pathname;
                        // Split the path into parts
                        var pathParts = currentPath.split('/');

                        // The last part should be the current page number, replace it with the new page number
                        if (!isNaN(pathParts[pathParts.length - 1])) {{
                            pathParts[pathParts.length - 1] = newPage;
                        }} else {{
                            // If the last part is not a number, assume it's missing and add the new page number
                            pathParts.push(newPage);
                        }}

                        // Join the path back together
                        var newPath = pathParts.join('/');
                        // Add any existing query parameters
                        var newUrl = newPath + window.location.search;
                        
                        // Navigate to the new URL
                        window.location.href = newUrl;
                    }}
                    </script>
                '''  
                return summary_table_html + table_html + pagination_html
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    @classmethod
    def query_job_status_list_for_data_product_id(cls, data_product_id, environment):
        """
        Executes the provided KQL query against Azure Application Insights using the provided parameters.
        Returns the query results.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("query_job_status_list_for_data_product_id"):
            try:
                if environment == "prod":
                    app_id = APPLICATIONINSIGHTS_APPLICATION_ID_PROD
                    api_key = APPLICATIONINSIGHTS_API_KEY_PROD
                else:
                    app_id = APPLICATIONINSIGHTS_APPLICATION_ID_DEV
                    api_key = APPLICATIONINSIGHTS_API_KEY_DEV

                query = f"""
                    let operations = dependencies
                    | extend jobName = tostring(customDimensions["job_name"]),
                            dataProductId = tolower(tostring(customDimensions["data_product_id"])),
                            environment = tostring(customDimensions["environment"]),
                            processLevel = tostring(customDimensions["process_level"])
                    | where tolower(dataProductId) == tolower("{data_product_id}") and processLevel == "child"
                    | summarize by operation_Id;
                    let operationDetails = dependencies
                    | extend jobName = tostring(customDimensions["job_name"]),
                            dataProductId = tolower(tostring(customDimensions["data_product_id"])),
                            environment = tostring(customDimensions["environment"]),
                            resultCode = toint(resultCode)
                    | project operation_Id, jobName, dataProductId, environment, resultCode, startTimestamp = timestamp, endTimestamp = timestamp
                    | summarize minTimestamp = min(startTimestamp),
                                maxTimestamp = max(endTimestamp),
                                jobName = max(jobName),
                                dataProductId = max(dataProductId),
                                environment = max(environment),
                                resultSuccess = minif(resultCode, resultCode == 0)
                        by operation_Id
                    | extend duration = maxTimestamp - minTimestamp;
                    let exceptionDetails = exceptions
                    | summarize firstExceptionTime = min(timestamp)
                        by operation_Id;
                    operations
                    | join kind=inner (operationDetails) on operation_Id
                    | join kind=leftouter (exceptionDetails) on operation_Id
                    | extend exceptionFlag = iff(isnotnull(firstExceptionTime), "Exception Occurred", "No Exception"),
                            exceptionSuccess = iff(isnull(firstExceptionTime) or firstExceptionTime == "", 1, 0)
                    | extend hasSuccess = resultSuccess == 0 and exceptionSuccess == 1
                    | extend status = iff(hasSuccess, "Success", "Failure")
                    | where jobName != ""
                    | order by maxTimestamp desc;
                """

                url = f"https://api.applicationinsights.io/v1/apps/{app_id}/query"
                headers = {
                    "x-api-key": api_key,
                    "Content-Type": "application/json"
                }
                params = {
                    "query": query
                }

                # Execute the query
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Raise an exception for bad status codes

                # Return the query results
                data = response.json()
                data = cls.convert_to_dict_list(data)

                for row in data:
                    if isinstance(row['maxTimestamp'], str):
                        # Example of format - adjust if the string format differs
                        row['maxTimestamp'] = datetime.strptime(row['maxTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')  
                    if isinstance(row['maxTimestamp'], datetime):
                        row['maxTimestamp'] = row['maxTimestamp'].strftime('%Y-%m-%d %I:%M %p')

                return data


            except Exception as ex:
                error_msg = f"Error executing KQL query: {ex}"
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, sys.exc_info())
                raise


    @classmethod
    def convert_to_dict_list(cls, data):
        if isinstance(data, dict) and "tables" in data and data["tables"]:
            rows = data["tables"][0]["rows"]
            columns = data["tables"][0]["columns"]

            # Extract "name" from columns if it's a dictionary, otherwise use the column value as-is
            processed_columns = [
                col["name"] if isinstance(col, dict) and "name" in col else col
                for col in columns
            ]
            
            # Proceed with converting rows into list of dictionaries
            return [dict(zip(processed_columns, row)) for row in rows]
        else:
            return []



    @staticmethod
    def query_ai_dependencies_by_operation_id(operation_id,  data_product_id, environment):

        from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
 
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("query_ai_dependencies_by_operation_id"):

            try:

                if environment == "prod":
                    app_id = APPLICATIONINSIGHTS_APPLICATION_ID_PROD
                    api_key = APPLICATIONINSIGHTS_API_KEY_PROD
                else:
                    app_id = APPLICATIONINSIGHTS_APPLICATION_ID_DEV
                    api_key = APPLICATIONINSIGHTS_API_KEY_DEV

                query = f"""
                dependencies
                | where operation_Id == '{operation_id}'
                | project timestamp, name, resultCode, duration, success
                | sort by timestamp asc
                """

                url = f"https://api.applicationinsights.io/v1/apps/{app_id}/query"
                headers = {
                    "x-api-key": api_key
                }
                params = {
                    "query": query
                }
                
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    return response.json()["tables"][0]["rows"]
                else:
                    raise ValueError(f"Error querying Application Insights: {response.text}")
                    return []
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    @staticmethod
    def query_ai_most_recent_child_dependency_by_parent_job_name(parent_job_name,  data_product_id, environment):

        from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
 
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("query_ai_most_recent_child_dependency_by_parent"):

            try:

                if environment == "prod":
                    app_id = APPLICATIONINSIGHTS_APPLICATION_ID_PROD
                    api_key = APPLICATIONINSIGHTS_API_KEY_PROD
                else:
                    app_id = APPLICATIONINSIGHTS_APPLICATION_ID_DEV
                    api_key = APPLICATIONINSIGHTS_API_KEY_DEV

                query = f"""
    dependencies
    | extend jobName = tostring(customDimensions["job_name"]),
             dataProductId = tostring(customDimensions["data_product_id"]),
             environment = tostring(customDimensions["environment"]),
             processLevel = tostring(customDimensions["process_level"]),
             parentId = operation_ParentId
    | where jobName == "{parent_job_name}"  
    | where processLevel == "child"  // Filter for the child process level
    | summarize maxTimestamp = max(timestamp) by operation_Id, name, type, target, resultCode, jobName, dataProductId, environment, processLevel
    | top 1 by maxTimestamp desc;  // Get the most recent child operation
                """

                url = f"https://api.applicationinsights.io/v1/apps/{app_id}/query"
                headers = {
                    "x-api-key": api_key
                }
                params = {
                    "query": query
                }
                
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    return response.json()["tables"][0]["rows"]
                else:
                    raise ValueError(f"Error querying Application Insights: {response.text}")
                    return []
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

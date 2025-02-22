import sys, os
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.databricks_service.dbx_db_rest import RestClient
from cdh_lava_core.databricks_service.dbx_rest.common import ApiContainer
from opentelemetry.trace.status import StatusCode, Status

# Get the currently running file name and parent folder name for logging purposes
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
SERVICE_NAME = os.path.basename(__file__)

class JobsClient(ApiContainer):
    """
    This class is responsible for managing jobs in Databricks, 
    including creating, running, fetching, and deleting jobs.
    """

    def __init__(self, client: RestClient):
        """
        Initializes the JobsClient with a Databricks client and configuration for logging.
        
        Args:
            client (RestClient): The RestClient object used to interact with the Databricks API.
        """
        self.client = client  # Client API exposing other operations to this class
        self.base_uri = f"{self.client.endpoint}/api/2.1/jobs"
        
        config = client.config
        # Initialize the logger
        data_product_id = config["data_product_id"]
        environment = config["environment"]
        self.tracer, self.logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

    def create(self, params, overwrite=False, run_now=False, lava_admin_user_or_role=None):
        """
        Creates a job in Databricks. If a job with the same name already exists and the overwrite flag is False, 
        the job creation is skipped. Optionally, the job can be run immediately if the `run_now` flag is True.
        
        Args:
            params (dict): The parameters for creating the job, including the job name and task details.
            overwrite (bool): If True, an existing job with the same name will be overwritten. Default is False.
            run_now (bool): If True, the job will be run immediately after being created. Default is False.
        
        Returns:
            dict: The result of the job creation API call or the existing job if not overwritten.
        """

        job_name = params.get("name", None)
                
        with self.tracer.start_as_current_span(f"create_job: {job_name}"):
            try:
                if job_name:
                    self.logger.info(f"Attempting to create job: {job_name}")
                    existing_job = self.get_by_name(job_name)
                    if existing_job and not overwrite:
                        self.logger.warning(f"Job '{job_name}' already exists. Skipping creation as overwrite is not set.")
                        return existing_job  # Return the existing job info instead of creating a new one

                # Create the job
                if "notebook_task" in params:
                    self.logger.warning("DEPRECATION WARNING: You are using the Jobs 2.0 version of create.")
                    result = self.create_2_0(params)
                else:
                    result = self.create_2_1(params)


                if lava_admin_user_or_role:
                    job_id = result.get("job_id")
                    self.client.permissions.jobs.share_job(job_id,lava_admin_user_or_role,"CAN_MANAGE")
                    
                # Run the job immediately if run_now is True
                if run_now:
                    job_id = result.get("job_id")
                    if job_id:
                        self.logger.info(f"Running job immediately with ID: {job_id}")
                        self.run_now(job_id)
                    else:
                        self.logger.error("Failed to retrieve job_id for immediate run.")

                return result

            except Exception as ex:
                error_msg = f"Error creating job: {ex}"
                exc_info = sys.exc_info()
                self.logger.exception(error_msg, exc_info=exc_info)
                raise

    def get_notebook_params(self, jobs_create_result):
        """
        Fetches the notebook parameters from the job creation result. If any of the expected keys are missing,
        it returns None.

        Args:
            jobs_create_result (dict): The result of the job creation API call.

        Returns:
            dict or None: The notebook parameters if available, otherwise None.
        """
        settings = jobs_create_result.get("settings", {})
        notebook_task = settings.get("notebook_task", {})
        base_parameters = notebook_task.get("base_parameters", None)
        
        return base_parameters

    def parse_job_name(self, job_name):
        # Split the job name by underscores
        parts = job_name.split("_")

        # Extract the data_product_id (everything before the second underscore)
        if len(parts) >= 2:
            data_product_id = "_".join(parts[:2])
        else:
            data_product_id = job_name  # Default to the whole job name if no second underscore is found

        # Extract the environment (everything after the last underscore)
        environment = parts[-1] if len(parts) > 1 else ""

        return data_product_id, environment
                        
    def create(self, params, overwrite=True, run_now=False):
        """
        Creates a job in Databricks. If a job with the same name already exists and the overwrite flag is False, 
        the job creation is skipped. Optionally, the job can be run immediately if the `run_now` flag is True.
        
        Args:
            params (dict): The parameters for creating the job, including the job name and task details.
            overwrite (bool): If True, an existing job with the same name will be overwritten. Default is False.
            run_now (bool): If True, the job will be run immediately after being created. Default is False.
        
        Returns:
            dict: The result of the job creation API call or the existing job if not overwritten.
        """


        # Add custom dimensions to the span
    
        job_name = params.get("name", None)
        lava_admin_user_or_role = params.get("lava_admin_user_or_role", None)
        del params["lava_admin_user_or_role"]
        
        with self.tracer.start_as_current_span(f"create_job: {job_name}") as job_span:

            data_product_id, environment = self.parse_job_name(job_name)
            job_span.set_attribute("job_name", job_name)
            job_span.set_attribute("data_product_id", data_product_id)
            job_span.set_attribute("environment", environment)
            job_span.set_attribute("process_level", "parent")

            try:
                jobs_create_result = None  # Initialize jobs_create_result to avoid referencing before assignment
                run_id = None  # Initialize run_id
                
                if job_name:
                    self.logger.info(f"Attempting to create job: {job_name}")
                    existing_job = self.get_by_name(job_name)

                    # If the job exists, handle according to the overwrite and run_now conditions
                    if existing_job:
                        if not overwrite and not run_now:
                            self.logger.warning(f"Job '{job_name}' already exists. Skipping creation as overwrite is not set.")
                            return existing_job  # Return the existing job info instead of creating a new one
                        elif overwrite:
                            self.logger.info(f"Overwriting existing job '{job_name}' as overwrite is set.")
                        jobs_create_result = existing_job  # Use the existing job if running immediately
                    else:
                        self.logger.info(f"No existing job found for '{job_name}'. Proceeding with job creation.")
                
                # If no existing job or overwrite is allowed, create the job
                if jobs_create_result is None:
                    if "notebook_task" in params:
                        self.logger.warning("DEPRECATION WARNING: You are using the Jobs 2.0 version of create.")
                        jobs_create_result = self.create_2_0(params)
                    else:
                        jobs_create_result = self.create_2_1(params)
                
                # Handle the case where job creation fails
                if jobs_create_result is None:
                    self.logger.error("jobs_create_result is None. Cannot proceed with job creation.")
                    raise ValueError("jobs_create_result is None, failed to create job.")

                if lava_admin_user_or_role:
                    job_id = jobs_create_result.get("job_id")
                    if job_id:
                        self.client.permissions.jobs.share_job(job_id, lava_admin_user_or_role, "CAN_MANAGE", data_product_id, environment)
                    else:
                        self.logger.error("Failed to retrieve job_id to set permissions.")
                
                # Run the job immediately if run_now is True
                if run_now:
                    job_id = jobs_create_result.get("job_id")
                    if job_id:
                        notebook_params = self.get_notebook_params(jobs_create_result)
                        self.logger.info(f"Running job immediately with ID: {job_id}")
                        run_id = self.run_now(job_id, notebook_params) if notebook_params else self.run_now(job_id)
                    else:
                        self.logger.error("Failed to retrieve job_id for immediate run.")
                
                job_span.set_status(Status(StatusCode.OK))
                return jobs_create_result, run_id

            except Exception as ex:
                error_msg = f"Error creating job: {ex}"
                self.logger.exception(error_msg)
                job_span.set_status(Status(StatusCode.ERROR, description=error_msg))
                job_span.end()
                raise

            
    def create_2_0(self, params):
        """
        Creates a job using the Databricks API 2.0 version.
        
        Args:
            params (dict): The parameters for creating the job.

        Returns:
            dict: The result of the job creation API 2.0 call.
        """
        with self.tracer.start_as_current_span("create_job_2_0"):
            try:
                self.logger.info("Creating job using API 2.0.")
                return self.client.execute_post_json(
                    f"{self.client.endpoint}/api/2.0/jobs/create", params
                )
            except Exception as ex:
                error_msg = f"Error creating job using API 2.0: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise   

    def create_2_1(self, params):
        """
        Creates a job using the Databricks API 2.1 version.
        
        Args:
            params (dict): The parameters for creating the job.

        Returns:
            dict: The result of the job creation API 2.1 call.
        """
        with self.tracer.start_as_current_span("create_job_2_1"):
            try:
                self.logger.info("Creating job using API 2.1.")
                return self.client.execute_post_json(
                    f"{self.client.endpoint.rstrip('/')}/api/2.1/jobs/create", params
                )
            except Exception as ex:
                error_msg = f"Error creating job using API 2.1: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

    def run_now(self, job_id: str, notebook_params: dict = None):
        """
        Immediately runs a Databricks job by its ID.
        
        Args:
            job_id (str): The ID of the job to run.
            notebook_params (dict): Additional notebook parameters to pass to the job when running.
        
        Returns:
            dict: The result of the job run API call.
        """
        with self.tracer.start_as_current_span("run_job_now"):
            try:
                self.logger.info(f"Running job: {job_id}")
                payload = {"job_id": job_id}
                if notebook_params is not None:
                    payload["notebook_params"] = notebook_params

                return self.client.execute_post_json(
                    f"{self.client.endpoint}/api/2.0/jobs/run-now", payload
                )
            except Exception as ex:
                error_msg = f"Error running job {job_id}: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

    def get(self, job_id):
        """
        Fetches details for a job by its ID.
        
        Args:
            job_id (str): The ID of the job to fetch.

        Returns:
            dict: The details of the job.
        """
        with self.tracer.start_as_current_span("get_job"):
            try:
                self.logger.info(f"Fetching details for job ID: {job_id}")
                return self.get_by_id(job_id)
            except Exception as ex:
                error_msg = f"Error fetching job {job_id}: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

    def get_by_id(self, job_id):
        """
        Fetches a job by its ID using the Databricks API.
        
        Args:
            job_id (str): The ID of the job to fetch.
        
        Returns:
            dict: The job details.
        """
        with self.tracer.start_as_current_span("get_job_by_id"):
            try:
                self.logger.info(f"Fetching job by ID: {job_id}")
                return self.client.execute_get_json(
                    f"{self.client.endpoint}/api/2.0/jobs/get?job_id={job_id}"
                )
            except Exception as ex:
                error_msg = f"Error fetching job by ID {job_id}: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

    def get_by_name(self, name: str):
        """
        Fetches a job by its name, searching through the list of jobs.
        
        Args:
            name (str): The name of the job to search for.
        
        Returns:
            dict: The job details if found, otherwise None.
        """
        with self.tracer.start_as_current_span("get_job_by_name"):
            try:
                self.logger.info(f"Searching for job by name: {name}")
                offset = 0
                limit = 25

                def search(jobs_list):
                    job_ids = [
                        j.get("job_id")
                        for j in jobs_list
                        if name == j.get("settings").get("name")
                    ]
                    return (
                        (False, None)
                        if len(job_ids) == 0
                        else (True, self.get_by_id(job_ids[0]))
                    )

                target_url = f"{self.client.endpoint}/api/2.1/jobs/list?limit={limit}"
                response = self.client.execute_get_json(target_url)
                jobs = response.get("jobs", list())

                found, job = search(jobs)
                if found:
                    return job

                while response.get("has_more", False):
                    offset += limit
                    response = self.client.execute_get_json(f"{target_url}&offset={offset}")
                    jobs = response.get("jobs", list())

                    found, job = search(jobs)
                    if found:
                        return job

                self.logger.warning(f"No job found with name: {name}")
                return None
            except Exception as ex:
                error_msg = f"Error fetching job by name {name}: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

    def delete_by_id(self, job_id):
        """
        Deletes a job by its ID.
        
        Args:
            job_id (str): The ID of the job to delete.
        """
        with self.tracer.start_as_current_span("delete_job_by_id"):
            try:
                self.logger.info(f"Deleting job by ID: {job_id}")
                self.client.execute_post_json(
                    f"{self.client.endpoint}/api/2.0/jobs/delete", {"job_id": job_id}
                )
            except Exception as ex:
                error_msg = f"Error deleting job by ID {job_id}: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

    def delete_by_name(self, job_names, success_only: bool):
        """
        Deletes jobs by their name, optionally deleting only successful jobs.
        
        Args:
            job_names (str, list, or dict): The name(s) of the jobs to delete.
            success_only (bool): If True, only jobs that were successfully completed will be deleted.
        """
        with self.tracer.start_as_current_span("delete_job_by_name"):
            try:
                if type(job_names) == dict:
                    job_names = list(job_names.keys())
                elif type(job_names) == list:
                    job_names = job_names
                elif type(job_names) == str:
                    job_names = [job_names]
                else:
                    raise TypeError(f"Unsupported type: {type(job_names)}")

                self.logger.info(f"Attempting to delete jobs by name: {job_names}")

                jobs = self.list()

                assert (
                    type(success_only) == bool
                ), f'Expected "success_only" to be of type "bool", found "{success_only}".'
                deleted = 0

                for job_name in job_names:
                    for job in jobs:
                        if job_name == job.get("settings").get("name"):
                            job_id = job.get("job_id")

                            runs = self.client.runs().list_by_job_id(job_id)
                            self.logger.info(f"Found {len(runs)} run(s) for job {job_id}")
                            delete_job = True

                            for run in runs:
                                state = run.get("state")
                                result_state = state.get("result_state", None)
                                life_cycle_state = state.get("life_cycle_state", None)

                                if success_only and life_cycle_state != "TERMINATED":
                                    delete_job = False
                                    self.logger.warning(
                                        f"""Job "{job_name}" is not TERMINATED but "{life_cycle_state}"."""
                                    )
                                if success_only and result_state != "SUCCESS":
                                    delete_job = False
                                    self.logger.warning(
                                        f"""Job "{job_name}" did not succeed (Result: "{result_state}")."""
                                    )

                            if delete_job:
                                self.logger.info(f'Deleting job #{job_id}, "{job_name}"')
                                for run in runs:
                                    run_id = run.get("run_id")
                                    self.logger.info(f"Deleting run #{run_id}")
                                    self.client.runs().delete(run_id)

                                self.delete_by_id(job_id)
                                deleted += 1

                self.logger.info(f"Deleted {deleted} job(s).")
            except Exception as ex:
                error_msg = f"Error deleting job by name: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.error_with_exception(error_msg, exc_info)
                raise

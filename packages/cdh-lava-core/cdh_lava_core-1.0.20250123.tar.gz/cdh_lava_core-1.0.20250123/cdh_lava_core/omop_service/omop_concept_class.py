import sys
import os
import pandas as pd

from cdh_lava_core.cdc_tech_environment_service.environment_http import EnvironmentHttp
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class OmopConceptClass:
    """
    Represents a class for fetching concepts from the Athena API.
    """

    BASE_URL = "https://athena.ohdsi.org/api/v1/concepts"
    DEFAULT_PAGE_SIZE = 100

    @staticmethod
    def fetch_concepts_by_query(
        query_string, page_size, data_product_id, environment, max_records=None
    ):
        """
        Fetches concepts from the OMOP database based on a query string.

        Args:
            query_string (str): The query string to search for concepts.
            page_size (int, optional): The number of concepts to fetch per page. Defaults to 100.
            data_product_id: The ID of the data product.
            environment: The environment to fetch concepts from.

        Returns:
            pandas.DataFrame: A DataFrame containing the fetched concepts.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("fetch_concepts_by_query"):
            try:

                # Validate page_size and adjust if necessary
                if isinstance(
                    page_size, (int, float)
                ):  # Checks if page_size is a number
                    if page_size > 1000:
                        page_size = 100
                    else:
                        page_size = (
                            100  # Set to 100 if non-numeric or not provided (None)
                        )
                else:
                    page_size = 100

                QUERY_TIMEOUT = 90

                df_columns = [
                    "id",
                    "code",
                    "name",
                    "className",
                    "standardConcept",
                    "invalidReason",
                    "domain",
                    "vocabulary",
                    "score",
                ]

                all_rows = []  # List to accumulate all rows
                page_num = 1

                obj_env_http = EnvironmentHttp()
                while True:
                    params = {
                        "pageSize": page_size,
                        "page": page_num,
                        "query": query_string,
                    }
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    }
                    response = obj_env_http.get_curl(
                        OmopConceptClass.BASE_URL,
                        headers=headers,
                        timeout=QUERY_TIMEOUT,
                        params=params,
                        data_product_id=data_product_id,
                        environment=environment,
                    )

                    response.raise_for_status()

                    data = response.json()
                    if data["empty"] or "content" not in data:
                        break

                    fetched_concepts = data["content"]
                    all_rows.extend(fetched_concepts)  # Add the items to the list
                    if len(fetched_concepts) < page_size or (
                        max_records is not None and len(all_rows) >= max_records
                    ):
                        break  # Exit if the last page or max_records reached

                    page_num += 1

                # Limit the rows if max_records is set
                if max_records is not None:
                    all_rows = all_rows[:max_records]

                # Create a DataFrame from the accumulated rows
                df = pd.DataFrame(all_rows, columns=df_columns)

                logger.info("Successfully fetched concepts by query.")

                return df

            except Exception as ex_:
                error_msg = "Error: %s", str(ex_)
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def fetch_concepts_for_class(
        concept_class, page_size, data_product_id: str, environment: str
    ):
        """
        Fetches all concepts for a given concept class with pagination.

        Args:
            concept_class (str): The concept class to fetch concepts for.
            page_size (int, optional): The number of concepts to fetch per page. Defaults to 100.

        Returns:
            pandas.DataFrame: A DataFrame containing the fetched concepts.
        """

        omop_concept_class_query = OmopConceptClass()

        # Validate page_size and adjust if necessary
        if isinstance(page_size, (int, float)):  # Checks if page_size is a number
            if page_size > 1000:
                page_size = 100
            else:
                page_size = 100  # Set to 100 if non-numeric or not provided (None)
        else:
            page_size = 100

        return omop_concept_class_query.fetch_concepts_by_query(
            f"class={concept_class}",
            page_size=page_size,
            data_product_id=data_product_id,
            environment=environment,
        )


# Example usage:
if __name__ == "__main__":
    # Fetch concepts by query
    omop_concept_class_query = OmopConceptClass()

    omop_concept_class_query = omop_concept_class_query.fetch_concepts_by_query(
        "aspirin", None, "reference_data", "dev"
    )
    print(omop_concept_class_query.head())

    # Fetch concepts for a specific class
    df_concepts_class = omop_concept_class_query.fetch_concepts_for_class(
        "Drug", 50, "reference_data", "dev"
    )
    print(df_concepts_class.head())

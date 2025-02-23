import requests

from leadmo_api.models.workflow_endpoint_params import GetWorkflowsParams
from leadmo_api.util import logger, _call_api, RETRIES, RETRY_DELAYS

LEADMO_API_V1_WORKFLOWS_URL = "https://rest.gohighlevel.com/v1/workflows/"


def get_workflows(
    api_key: str, params: GetWorkflowsParams = None, retries=RETRIES["get_workflows"], retry_delay=RETRY_DELAYS["get_workflows"]
) -> requests.Response:
    """
    Retrieve appointments associated with a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetWorkflowsParams): Parameters for the API call.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the contact appointments information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    if not params:
        logger.info("No params provided. Getting all workflows.")

    url = LEADMO_API_V1_WORKFLOWS_URL
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to get workflows: {e}")
        raise

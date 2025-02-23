import os
import time
import boto3
import requests
from aws_lambda_powertools import Logger
from collections import defaultdict
from dateutil import parser
from dateutil.tz import tz

DEFAULT_ORIGIN = os.getenv("DEFAULT_ORIGIN", "https://localhost:5173")
APP_NAME = os.getenv("APP_NAME", "augint-tools")

DEFAULT_RETRY_DELAY = 500
DEFAULT_RETRY_COUNT = 0

RETRIES: defaultdict[str, int] = defaultdict(lambda: DEFAULT_RETRY_COUNT)
RETRIES["lookup_contact"] = 3
RETRIES["get_contact_by_id"] = 3
RETRIES["update_contact"] = 2
RETRIES["get_contact_appointments"] = 3
RETRIES["get_custom_fields"] = 3
RETRIES["remove_tag_from_contact"] = 3
RETRIES["get_available_appointment_slots"] = 3
RETRIES["get_appointment_by_id"] = 3
RETRIES["get_appointments"] = 3
RETRIES["delete_appointment"] = 3

RETRY_DELAYS: defaultdict[str, int] = defaultdict(lambda: DEFAULT_RETRY_DELAY)
RETRY_DELAYS["update_contact"] = 1000
RETRY_DELAYS["delete_appointment"] = 1000


def _call_api(
    api_key: str,
    url: str,
    method: str,
    json_data: dict = None,
    params=None,
    retries=DEFAULT_RETRY_COUNT,
    retry_delay=DEFAULT_RETRY_DELAY,
) -> requests.Response:
    """
    Call the Lead Momentum API using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        url (str): The URL for the API endpoint.
        method (str): The HTTP method to use for the request.
        json_data (dict, optional): The JSON data to include in the request body. Defaults to None.

    Returns:
        requests.Response: The API response containing the requested information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    headers = get_headers(api_key)
    verb = method.lower()
    func = getattr(requests, verb)
    json_data = json_data or {}
    params = params or {}

    remaining_retries = retries + 1
    while remaining_retries > 0:
        # for remaining_retries in range(retries + 1)[::-1]:
        try:
            response = func(url=url, headers=headers, json=json_data, params=params)
            response.raise_for_status()
            logger.debug("API call successful")
            return response
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            remaining_retries -= 1
            if remaining_retries > 0:
                # logger.warning(f"Encountered exception: {e}")
                logger.info(f"Retrying in {retry_delay} ms.")
                time.sleep(retry_delay / 1000)
                continue
            else:
                logger.error(f"Failure calling API after ({retries}) retries with a delay of ({retry_delay}): {e}")
                raise
    raise


def get_logger() -> Logger:
    log_level = os.environ.get("LOG_LEVEL", "INFO")  # Default to INFO if not set
    _logger = Logger(service=f"{APP_NAME}", level=log_level)
    return _logger


def get_headers(api_key: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    return headers


def iso_to_epoch(iso: str, timezone: str = "UTC") -> int:
    """
    Convert an ISO formatted timestamp to an epoch timestamp.

    Args:
        iso: The ISO formatted timestamp.
        timezone: The timezone of the timestamp. Default is 'UTC'.

    Returns:
        The epoch timestamp.
    """
    standardized_tz = tz.gettz(timezone)
    standardized_time = parser.parse(iso).astimezone(standardized_tz)
    epoch = int(standardized_time.timestamp() * 1000)
    return epoch


def put_metric_data(metric_name, value, dimensions, namespace):
    cloudwatch = boto3.client("cloudwatch")
    cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                "MetricName": metric_name,
                "Dimensions": dimensions,
                "Value": value,
            },
        ],
    )


logger = get_logger()

import json
import requests

from leadmo_api.models.appointment_endpoint_params import (
    GetAppointmentSlotsParams,
    CreateAppointmentParams,
    GetAppointmentByIdParams,
    GetAppointmentsParams,
    DeleteAppointmentParams,
    UpdateAppointmentParams,
    UpdateAppointmentStatusParams,
)
from leadmo_api.util import logger, _call_api, RETRIES, RETRY_DELAYS

LEADMO_API_V1_APPOINTMENTS_URL = "https://rest.gohighlevel.com/v1/appointments/"
LEADMO_API_V1_GET_APPOINTMENT_SLOTS_URL = "https://rest.gohighlevel.com/v1/appointments/slots/"


def get_available_appointment_slots(
    api_key: str,
    params: GetAppointmentSlotsParams,
    retries=RETRIES["get_available_appointment_slots"],
    retry_delay=RETRY_DELAYS["get_available_appointment_slots"],
) -> requests.Response:
    """
    Retrieve available appointment slots using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetAppointmentSlotsParams): Parameters for retrieving appointment slots.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing available appointment slots.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    get_appointment_slots_dict = params.model_dump(by_alias=True)
    url = LEADMO_API_V1_GET_APPOINTMENT_SLOTS_URL
    try:
        return _call_api(api_key, url, "GET", params=get_appointment_slots_dict, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving available appointment slots: {e}")
        raise


def create_appointment(
    api_key: str,
    params: CreateAppointmentParams,
    retries=RETRIES["create_appointment"],
    retry_delay=RETRY_DELAYS["create_appointment"],
) -> requests.Response:
    """
    Create a new appointment using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (CreateAppointmentParams): Parameters required for creating an appointment.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the created appointment information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    contact_data_json = params.model_dump_json(by_alias=True)
    json_data = json.loads(contact_data_json)
    url = LEADMO_API_V1_APPOINTMENTS_URL
    try:
        return _call_api(api_key, url, "POST", json_data=json_data, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating appointment: {e}")
        logger.error(f"{e.response}")
        raise


def get_appointment_by_id(
    api_key: str,
    params: GetAppointmentByIdParams,
    retries=RETRIES["get_appointment_by_id"],
    retry_delay=RETRY_DELAYS["get_appointment_by_id"],
) -> requests.Response:
    """
    Retrieve an appointment by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetAppointmentByIdParams): Parameters containing the appointment ID.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the appointment information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{params.appointment_id}"

    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Endpoint error retrieving appointment by ID: {e}")
        raise


def get_appointments(
    api_key: str, params: GetAppointmentsParams, retries=RETRIES["get_appointments"], retry_delay=RETRY_DELAYS["get_appointments"]
) -> requests.Response:
    """
    Retrieve appointments based on the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetAppointmentsParams): Parameters for retrieving appointments.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the appointments information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    get_appointments_dict = params.model_dump(by_alias=True)
    url = LEADMO_API_V1_APPOINTMENTS_URL
    try:
        return _call_api(api_key, url, "GET", params=get_appointments_dict, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving appointments: {e}")
        raise


def delete_appointment(
    api_key: str,
    params: DeleteAppointmentParams,
    retries=RETRIES["delete_appointment"],
    retry_delay=RETRY_DELAYS["delete_appointment"],
) -> requests.Response:
    """
    Delete an appointment by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (DeleteAppointmentParams): Parameters containing the appointment ID.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response confirming the appointment deletion.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{params.appointment_id}"

    try:
        return _call_api(api_key, url, "DELETE", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting appointment: {e}")
        raise


def update_appointment(
    api_key: str,
    params: UpdateAppointmentParams,
    retries=RETRIES["update_appointment"],
    retry_delay=RETRY_DELAYS["update_appointment"],
) -> requests.Response:
    """
    Update an existing appointment using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (UpdateAppointmentParams): Parameters for updating an appointment.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the updated appointment information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    appointment_data = params.model_dump(by_alias=True)
    appointment_id = appointment_data.pop("appointmentId")
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{appointment_id}"

    try:
        return _call_api(api_key, url, "PUT", json_data=appointment_data, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating appointment: {e}")
        raise


def update_appointment_status(
    api_key: str, params: UpdateAppointmentStatusParams, retries=0, retry_delay=500
) -> requests.Response:
    """
    Update the status of an appointment.

    Args:
        api_key (str): The API key for authenticating requests.
        params (UpdateAppointmentStatusParams): Parameters for updating the appointment status.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response confirming the status update.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    appointment_data = params.model_dump(by_alias=True)
    appointment_id = appointment_data.pop("appointmentId")
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{appointment_id}/status"

    try:
        return _call_api(api_key, url, "PUT", json_data=appointment_data, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating appointment status: {e}")
        raise

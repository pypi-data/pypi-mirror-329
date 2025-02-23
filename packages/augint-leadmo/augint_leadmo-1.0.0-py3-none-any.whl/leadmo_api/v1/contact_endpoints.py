import json
import urllib.request
import requests

from leadmo_api.models.contact_endpoint_params import (
    CreateContactParams,
    UpdateContactParams,
    LookupContactParams,
    DeleteContactParams,
    GetContactByIdParams,
    GetContactAppointmentsParams,
    TagContactParams,
    RemoveTagFromContactParams,
    AddContactToWorkflowParams,
    GetCustomFieldsParams,
)
from leadmo_api.util import logger, _call_api, RETRY_DELAYS, RETRIES

# Predefined URL constants
LEADMO_API_V1_CONTACTS_URL = "https://rest.gohighlevel.com/v1/contacts/"
LEADMO_API_V1_LOOKUP_CONTACT_URL = "https://rest.gohighlevel.com/v1/contacts/lookup"
LEADMO_API_V1_CUSTOM_FIELDS_URL = "https://rest.gohighlevel.com/v1/custom-fields/"


def create_contact(
    api_key: str, params: CreateContactParams, retries=RETRIES["create_contact"], retry_delay=RETRY_DELAYS["create_contact"]
) -> requests.Response:
    """
    Create a new contact using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (CreateContactParams): Parameters required for creating a contact.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the created contact information.

    Raises:
        ValueError: If neither 'email' nor 'phone' is provided.
        requests.exceptions.RequestException: If the request fails.
    """
    contact_data_json = params.model_dump_json(by_alias=True)
    json_data = json.loads(contact_data_json)

    try:
        return _call_api(api_key, LEADMO_API_V1_CONTACTS_URL, "POST", json_data, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise


def lookup_contact(
    api_key: str, params: LookupContactParams, retries=RETRIES["lookup_contact"], retry_delay=RETRY_DELAYS["lookup_contact"]
) -> requests.Response:
    """
    Lookup a contact using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (LookupContactParams): Parameters for looking up a contact.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the contact information.

    Raises:
        ValueError: If neither 'email' nor 'phone' is provided.
        requests.exceptions.RequestException: If the request fails.
    """
    params = params.model_dump(by_alias=True)
    params_str = "&".join([f"{k}={urllib.request.pathname2url(v)}" for k, v in params.items() if v is not None])
    url = f"{LEADMO_API_V1_LOOKUP_CONTACT_URL}?{params_str}"

    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error looking up contact: {e}")
        raise


def get_contact_by_id(
    api_key: str,
    params: GetContactByIdParams,
    retries=RETRIES["get_contact_by_id"],
    retry_delay=RETRY_DELAYS["get_contact_by_id"],
) -> requests.Response:
    """
    Retrieve a contact by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetContactByIdParams): Parameters containing the contact ID.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the contact information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}"
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error retrieving contact by ID: {e}")
        raise


def update_contact(
    api_key: str, params: UpdateContactParams, retries=RETRIES["update_contact"], retry_delay=RETRY_DELAYS["update_contact"]
) -> requests.Response:
    """
    Update an existing contact using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (UpdateContactParams): Parameters for updating a contact.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the updated contact information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    if not params.contact_id:
        lookup_contact_response = lookup_contact(api_key, LookupContactParams(**params.model_dump(by_alias=True)))
        first_contact = lookup_contact_response.json().get("contacts")[0]
        params.contact_id = first_contact.get("id")

    contact_data_json = params.model_dump_json(by_alias=True)
    json_data = json.loads(contact_data_json)
    contact_id = json_data.pop("contactId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}"

    try:
        return _call_api(api_key, url, "PUT", json_data, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error updating contact: {e}")
        raise


def delete_contact(
    api_key: str, params: DeleteContactParams, retries=RETRIES["delete_contact"], retry_delay=RETRY_DELAYS["delete_contact"]
) -> requests.Response:
    """
    Delete a contact by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (DeleteContactParams): Parameters containing the contact ID.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response confirming the contact deletion.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    if not params.contact_id:
        logger.info(f"Contact ID not provided. Looking up contact to get ID using {params}")
        try:
            lookup_contact_response = lookup_contact(api_key, LookupContactParams(**params.model_dump(by_alias=True)))
            first_contact = lookup_contact_response.json().get("contacts")[0]
            params.contact_id = first_contact.get("id")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                logger.info(f"Contact does not exist: {params.contact_id}")
                return e.response
            else:
                logger.error(f"HTTP error deleting contact: {e}")
                raise
        except Exception as e:
            logger.error(f"Unknown error deleting contact: {e}")
            raise

    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}"
    try:
        return _call_api(api_key, url, "DELETE", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            logger.info(f"Contact does not exist: {params.contact_id}")
        else:
            logger.error(f"HTTP error deleting contact: {e}")
            raise
    except Exception as e:
        logger.error(f"Unknown error deleting contact: {e}")
        raise


def get_contact_appointments(
    api_key: str,
    params: GetContactAppointmentsParams,
    retries=RETRIES["get_contact_appointments"],
    retry_delay=RETRY_DELAYS["get_contact_appointments"],
) -> requests.Response:
    """
    Retrieve appointments associated with a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetContactAppointmentsParams): Parameters containing the contact ID.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the contact appointments information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}/appointments/"
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error retrieving contact appointments: {e}")
        raise


def tag_contact(
    api_key: str, params: TagContactParams, retries=RETRIES["tag_contact"], retry_delay=RETRY_DELAYS["tag_contact"]
) -> requests.Response:
    """
    Add tags to a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (TagContactParams): Parameters for adding tags to a contact.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response confirming the addition of tags.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    params_dict = params.model_dump(by_alias=True)
    contact_id = params_dict.pop("contactId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}/tags"

    try:
        return _call_api(api_key, url, "POST", json_data=params_dict, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error adding tags to contact: {e}")
        raise


def remove_tag_from_contact(
    api_key: str,
    params: RemoveTagFromContactParams,
    retries=RETRIES["remove_tag_from_contact"],
    retry_delay=RETRY_DELAYS["remove_tag_from_contact"],
) -> requests.Response:
    """
    Remove tags from a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (RemoveTagFromContactParams): Parameters for removing tags from a contact.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response confirming the removal of tags.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    params_dict = params.model_dump(by_alias=True)
    contact_id = params_dict.pop("contactId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}/tags"

    try:
        return _call_api(api_key, url, "DELETE", json_data=params_dict, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error removing tags from contact: {e}")
        raise


def add_contact_to_workflow(
    api_key: str,
    params: AddContactToWorkflowParams,
    retries=RETRIES["add_contact_to_workflow"],
    retry_delay=RETRY_DELAYS["add_contact_to_workflow"],
) -> requests.Response:
    """
    Add a contact to a workflow.

    Args:
        api_key (str): The API key for authenticating requests.
        params (AddContactToWorkflowParams): Parameters for adding a contact to a workflow.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response confirming the addition to the workflow.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    params_dict = params.model_dump(by_alias=True)
    contact_id = params_dict.pop("contactId")
    workflow_id = params_dict.pop("workflowId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}/workflow/{workflow_id}"

    try:
        return _call_api(api_key, url, "POST", json_data=params_dict, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error adding contact to workflow: {e}")
        raise


def get_custom_fields(
    api_key: str,
    params: GetCustomFieldsParams,
    retries=RETRIES["get_custom_fields"],
    retry_delay=RETRY_DELAYS["get_custom_fields"],
) -> requests.Response:
    """
    Retrieve custom all available custom fields.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetCustomFieldsParams): No params.
        retries (int): Number of retry attempts in case of failure.
        retry_delay (int): Delay between retry attempts in milliseconds.

    Returns:
        requests.Response: The API response containing the contact appointments information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = LEADMO_API_V1_CUSTOM_FIELDS_URL
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.error(f"Error retrieving contact custom fields information: {e}")
        raise

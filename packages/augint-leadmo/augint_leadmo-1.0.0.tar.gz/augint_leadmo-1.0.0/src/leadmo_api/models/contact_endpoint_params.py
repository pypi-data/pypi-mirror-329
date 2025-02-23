from __future__ import annotations

from datetime import datetime

import pytz
from pydantic import Field, EmailStr, HttpUrl, constr, StrictStr, field_validator
from typing import Optional, List, Dict
from leadmo_api.models.common import BaseLeadmoApiCallModel


def now_string_factory():
    current_time = datetime.now(pytz.utc)
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    formatted_time = formatted_time[:-2] + ":" + formatted_time[-2:]
    return formatted_time


class WithContactId(BaseLeadmoApiCallModel):
    """
    Model representing a parameter with a contact ID.

    Attributes:
        contact_id (Optional[StrictStr]): The unique identifier for a contact.
            This ID is used to reference a specific contact within the system.
    """

    contact_id: Optional[StrictStr] = Field(
        None,
        description="The unique identifier for a contact. This ID is used to reference a specific contact within the system.",
    )


class WithContactCommonFields(BaseLeadmoApiCallModel):
    """
    Model representing common contact fields used across different operations.

    Attributes:
        email (Optional[EmailStr]): Email address of the contact. Must be a valid email format.
        phone (Optional[constr]): Phone number of the contact. Must be in E.164 format with a leading '+' sign.
    """

    email: Optional[EmailStr] = Field(None, description="Email address of the contact. Must be a valid email format.")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(
        None, description="Phone number of the contact. Must be in E.164 format with a leading '+' sign."
    )


class WithTags(BaseLeadmoApiCallModel):
    """
    Model representing tags associated with a contact.

    Attributes:
        tags (Optional[List[constr]]): List of tags associated with the contact. Tags are stored in lowercase and are case-insensitive.
    """

    tags: Optional[List[constr(to_lower=True)]] = Field(
        None, description="List of tags associated with the contact. Tags are stored in lowercase and are case-insensitive."
    )


class WithContactDetails(WithContactCommonFields, WithTags):
    """
    Model representing detailed contact information.

    Attributes:
        location_id (Optional[StrictStr]): Identifier for the contact's location. Used to reference a specific location in the system.
        first_name (Optional[StrictStr]): First name of the contact.
        last_name (Optional[StrictStr]): Last name of the contact.
        name (Optional[StrictStr]): Full name of the contact. If provided, it should be used in place of first and last names.
        address1 (Optional[StrictStr]): Primary address line of the contact.
        city (Optional[StrictStr]): City where the contact is located.
        state (Optional[StrictStr]): State where the contact is located.
        postal_code (Optional[StrictStr]): Postal code for the contact's address.
        website (Optional[HttpUrl]): URL of the contact's website.
        timezone (Optional[StrictStr]): Timezone of the contact, represented as a string.
        dnd (Optional[bool]): Do Not Disturb status for the contact. If True, the contact should not be contacted.
        custom_field (Optional[Dict[StrictStr, StrictStr]]): Custom fields for the contact. This is a dictionary where keys and values are both strings.
        source (Optional[StrictStr]): Source of the contact, such as a form, manual entry, etc.
    """

    location_id: Optional[StrictStr] = Field(
        None, description="Identifier for the contact's location. Used to reference a specific location in the system."
    )
    first_name: Optional[StrictStr] = Field(None, description="First name of the contact.")
    last_name: Optional[StrictStr] = Field(None, description="Last name of the contact.")
    name: Optional[StrictStr] = Field(
        None, description="Full name of the contact. If provided, it should be used in place of first and last names."
    )
    address1: Optional[StrictStr] = Field(None, description="Primary address line of the contact.")
    city: Optional[StrictStr] = Field(None, description="City where the contact is located.")
    state: Optional[StrictStr] = Field(None, description="State where the contact is located.")
    postal_code: Optional[StrictStr] = Field(None, description="Postal code for the contact's address.")
    website: Optional[HttpUrl] = Field(None, description="URL of the contact's website.")
    timezone: Optional[StrictStr] = Field(None, description="Timezone of the contact, represented as a string.")
    dnd: Optional[bool] = Field(
        None, description="Do Not Disturb status for the contact. If True, the contact should not be contacted."
    )
    custom_field: Optional[Dict[StrictStr, StrictStr]] = Field(
        None, description="Custom fields for the contact. This is a dictionary where keys and values are both strings."
    )
    source: Optional[StrictStr] = Field(None, description="Source of the contact, such as a form, manual entry, etc.")

    @field_validator("tags", "custom_field", mode="before")
    def check_not_empty(cls, v):
        """
        Ensure that no empty strings are allowed in tags or custom fields.

        Args:
            v: The value to check.

        Returns:
            The original value if not empty.

        Raises:
            ValueError: If the value is an empty string.
        """
        if v is not None and isinstance(v, str) and not v.strip():
            raise ValueError("Empty strings are not allowed")
        return v


class CreateContactParams(WithContactDetails):
    """
    Parameters required for creating a new contact. Inherits common contact fields and tags.
    """

    pass


class UpdateContactParams(WithContactDetails, WithContactId):
    """
    Parameters required for updating an existing contact.

    Must provide at least one identifier (contact_id, email, or phone).

    Raises:
        ValueError: If none of contact_id, email, or phone is provided.
    """

    def __post_init__(self):
        if self.contact_id is None and self.email is None and self.phone is None:
            raise ValueError("One of contact_id, email, or phone must be provided")


class LookupContactParams(WithContactCommonFields):
    """
    Parameters for looking up a contact by common fields such as email or phone.
    """

    pass


class GetContactByIdParams(WithContactId):
    """
    Parameters for retrieving a contact by its unique identifier.
    """

    pass


class DeleteContactParams(WithContactCommonFields, WithContactId):
    """
    Parameters for deleting a contact.

    Must provide at least one identifier (contact_id, email, or phone).

    Raises:
        ValueError: If none of contact_id, email, or phone is provided.
    """

    def __post_init__(self):
        if self.contact_id is None and self.email is None and self.phone is None:
            raise ValueError("One of contact_id, email, or phone must be provided")


class GetContactAppointmentsParams(WithContactId):
    """
    Parameters for retrieving appointments associated with a specific contact by ID.
    """

    pass


class TagContactParams(WithContactId, WithTags):
    """
    Parameters for adding tags to a specific contact identified by ID.
    """

    pass


class RemoveTagFromContactParams(WithContactId, WithTags):
    """
    Parameters for removing tags from a specific contact identified by ID.
    """

    pass


class AddContactToWorkflowParams(WithContactId):
    """
    Parameters for adding a contact to a workflow.

    Attributes:
        workflow_id (StrictStr): The unique identifier of the workflow to which the contact will be added.
        event_start_time (Optional[StrictStr]): The time the event should start. The system will use this to schedule the event near the specified time.
    """

    workflow_id: StrictStr = Field(..., description="The unique identifier of the workflow to which the contact will be added.")
    event_start_time: Optional[StrictStr] = Field(
        default_factory=now_string_factory,
        description="The time the event should start. The system will use this to schedule the event near the specified time.",
    )


class GetCustomFieldsParams(BaseLeadmoApiCallModel):
    """
    Parameters for retrieving available custom fields.
    """

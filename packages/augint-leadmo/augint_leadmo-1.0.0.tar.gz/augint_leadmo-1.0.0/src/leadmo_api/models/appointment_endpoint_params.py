from __future__ import annotations

from datetime import datetime, timedelta

from dateutil.parser import ParserError
from pydantic import Field, EmailStr, HttpUrl, constr, StrictStr, field_validator
from typing import Optional, Dict
from leadmo_api.models.common import BaseLeadmoApiCallModel
from leadmo_api.util import iso_to_epoch, logger


class WithCalendarId(BaseLeadmoApiCallModel):
    """
    Model representing a parameter with a calendar ID.

    Attributes:
        calendar_id (Optional[StrictStr]): The unique identifier for a calendar.
            Used to reference a specific calendar within the system.
    """

    calendar_id: Optional[StrictStr] = Field(None, description="The calendar ID")


class WithAppointmentId(BaseLeadmoApiCallModel):
    """
    Model representing a parameter with an appointment ID.

    Attributes:
        appointment_id (Optional[StrictStr]): The unique identifier for an appointment.
            Used to reference a specific appointment within the system.
    """

    appointment_id: Optional[StrictStr] = Field(None, description="The appointment ID")


class WithStartAndEndDate(BaseLeadmoApiCallModel):
    """
    Model representing parameters with start and end dates.

    Attributes:
        start_date (StrictStr): Epoch timestamp representing the start date.
        end_date (StrictStr): Epoch timestamp representing the end date.
    """

    start_date: StrictStr = Field(
        default_factory=datetime.now, description="ISO timestamp representing the start date", validate_default=True
    )
    end_date: StrictStr = Field(
        default_factory=lambda: (datetime.now() + timedelta(days=5)),
        description="ISO timestamp representing the end date",
        validate_default=True,
    )

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def validate_dates(cls, date):

        if isinstance(date, datetime):
            return str(int(date.timestamp() * 1000))

        elif isinstance(date, str):
            try:
                # If this is an ISO timestamp, this will convert it to the type of epoch Leadmo accepts
                return str(iso_to_epoch(date))
            except OverflowError as e:
                # If an exception was raised, then we assume this is already an epoch timestamp
                logger.warning(f"Failed to parse date {date} as ISO timestamp, assuming it's already a proper timestamp: {e}")
                return date
            except ParserError as e:
                logger.error(f"Failed to parse date {date} as ISO timestamp: {e}")
                raise

        elif isinstance(date, int):
            return str(date)

        else:
            raise ValueError(f"Date {date} must be a string, datetime, or integer")


class WithCalendarDetails(BaseLeadmoApiCallModel):
    """
    Model representing details of a calendar.

    Attributes:
        selected_slot (Optional[StrictStr]): The selected slot for the appointment, e.g., "2021-02-05T11:00:00+05:30".
        selected_timezone (Optional[StrictStr]): The selected timezone for the appointment. Default is "UTC".
        calendar_notes (Optional[StrictStr]): Notes for the appointment.
    """

    selected_slot: Optional[StrictStr] = Field(
        None, description="The selected slot for the appointment - example: 2021-02-05T11:00:00+05:30"
    )
    selected_timezone: Optional[StrictStr] = Field(
        "UTC", description="The selected timezone for the appointment - default: US/Eastern"
    )
    calendar_notes: Optional[StrictStr] = Field(None, description="Notes for the appointment")


class CreateAppointmentParams(WithCalendarId, WithCalendarDetails):
    """
    Parameters required for creating a new appointment.

    Attributes:
        email (Optional[EmailStr]): Email of the contact. One of email or phone must be provided.
        phone (Optional[constr]): Phone number of the contact. Must be in E.164 format with a leading '+' sign.
        title (Optional[str]): Title of the appointment.
        first_name (Optional[StrictStr]): The contact's first name.
        last_name (Optional[StrictStr]): The contact's last name.
        name (Optional[StrictStr]): The contact's full name.
        address1 (Optional[StrictStr]): The contact's address line 1.
        city (Optional[StrictStr]): The contact's city.
        state (Optional[StrictStr]): The contact's state.
        website (Optional[HttpUrl]): The contact's website.
        custom_field (Optional[Dict[StrictStr, StrictStr]]): The contact's custom fields.

    Raises:
        ValueError: If neither email nor phone is provided.
    """

    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")

    # Optional
    title: Optional[str] = Field(None, description="Title of the appointment")
    first_name: Optional[StrictStr] = Field(None, description="The contact's first name")
    last_name: Optional[StrictStr] = Field(None, description="The contact's last name")
    name: Optional[StrictStr] = Field(None, description="The contact's full name")
    address1: Optional[StrictStr] = Field(None, description="The contact's address line 1")
    city: Optional[StrictStr] = Field(None, description="The contact's city")
    state: Optional[StrictStr] = Field(None, description="The contact's state")
    website: Optional[HttpUrl] = Field(None, description="The contact's website")
    custom_field: Optional[Dict[StrictStr, StrictStr]] = Field(None, description="The contact's custom fields")

    @field_validator("custom_field", mode="before")
    def check_not_empty(cls, v):
        """
        Ensure that no empty strings are allowed in custom fields.

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

    def __post_init__(self):
        if self.email is None and self.phone is None:
            raise ValueError("One of email or phone must be provided")


class GetAppointmentSlotsParams(WithCalendarId, WithStartAndEndDate):
    """
    Parameters for retrieving available appointment slots.

    Attributes:
        user_id (Optional[StrictStr]): User ID associated with the calendar.
        timezone (Optional[StrictStr]): Timezone for the start and end dates.
    """

    user_id: Optional[StrictStr] = Field(None, description="User ID")
    timezone: Optional[StrictStr] = Field("UTC", description="Timezone for the start and end dates")


class GetAppointmentsParams(WithCalendarId, WithStartAndEndDate):
    """
    Parameters for retrieving appointments.

    Attributes:
        team_id (Optional[StrictStr]): The team ID for the appointments to get.
        user_id (Optional[StrictStr]): The user ID associated with the appointments to retrieve.
        include_all (Optional[bool]): Include contact and more data. Default is False.

    Raises:
        ValueError: If none of calendar_id, team_id, or user_id is provided.
    """

    team_id: Optional[StrictStr] = Field(None, description="The team ID for the appointments to get")
    user_id: Optional[StrictStr] = Field(None, description="The user ID associated with the appointments to retrieve")

    include_all: Optional[bool] = Field(False, description="Include contact and more data")

    def __post_init__(self):
        if self.calendar_id is None and self.team_id is None and self.user_id is None:
            raise ValueError("One of user_id, team_id, or calendar_id must be provided")


class UpdateAppointmentStatusParams(WithAppointmentId):
    """
    Parameters for updating the status of an appointment.

    Attributes:
        status (StrictStr): The status of the appointment. Must be one of 'confirmed', 'cancelled', 'showed', 'noshow', or 'invalid'.

    Raises:
        ValueError: If status is not one of the allowed values.
    """

    status: StrictStr = Field("confirmed", description="The status of the appointment")

    def __post_init__(self):
        valid_statuses = ["confirmed", "cancelled", "showed", "noshow", "invalid"]
        if self.status not in valid_statuses:
            raise ValueError("status must be one of 'confirmed', 'cancelled', 'showed', 'noshow', or 'invalid'")


class GetAppointmentByIdParams(WithAppointmentId):
    """
    Parameters for retrieving an appointment by its unique identifier.
    """

    pass


class DeleteAppointmentParams(WithAppointmentId):
    """
    Parameters for deleting an appointment by its unique identifier.
    """

    pass


class UpdateAppointmentParams(WithAppointmentId, WithCalendarDetails):
    """
    Parameters for updating an appointment's details.

    Inherits calendar details such as selected slot, timezone, and notes.
    """

    pass

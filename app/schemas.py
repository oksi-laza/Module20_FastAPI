from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional


class ContactCreate(BaseModel):
    """The pydantic model for recording contacts of a potential client: his name, phone number and email address"""
    name: str
    phone: str = Field(..., max_length=20)
    email: Optional[str] = None
    privacy_policy_consent: bool = True


class ContactResponse(BaseModel):
    """
    The pydantic model for obtaining information about a potential client:
    his name, phone number and email address, as well as the time when the record was created.
    """
    id: int
    name: str
    phone: str
    email: str
    privacy_policy_consent: bool = True
    created_at: datetime


class MeetingAtOfficeCreate(BaseModel):
    """The pydantic model for creating an appointment for a selected date and time."""
    first_name: str
    last_name: str
    phone: str = Field(..., max_length=20)
    date_of_meeting: str = Field(..., pattern=r'^\d{2}\.\d{2}\.\d{4}$', description='Дата в формате дд.мм.гггг')
    meeting_time: time
    privacy_policy_consent: bool = True


class MeetingAtOfficeUpdate(BaseModel):
    """
    The pydantic model for making changes to the previous appointment record,
    namely the date and time of the meeting with a previously recorded client.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_meeting: str = Field(..., pattern=r'^\d{2}\.\d{2}\.\d{4}$', description='Дата в формате дд.мм.гггг')
    meeting_time: time
    privacy_policy_consent: bool = True


class MeetingAtOfficeResponse(BaseModel):
    """The pydantic model for getting information about appointments with potential clients."""
    id: int
    first_name: str
    last_name: str
    phone: str
    date_of_meeting: str
    meeting_time: time
    created_at: datetime
    updated_at: datetime
    privacy_policy_consent: bool


class ServicesOfferedCreateUpdate(BaseModel):
    """
    The pydantic model for working with information about the services provided by the company,
    adding or changing services and photos.
    """
    title: str = Field(..., max_length=60)
    link_to_photo: str = Field(..., max_length=200)


class InfoGlavnoeCreateUpdate(BaseModel):
    """
    The pydantic model for working with information about the specifics of the company's work,
    adding and changing this information.
    """
    title: str = Field(..., max_length=100)
    description: str


class FoundationsCreateUpdate(BaseModel):
    """
    The pydantic model is designed to work with a block of information
    about the foundations that the company is building, adding and removing descriptions and photos.
    """
    title: str = Field(..., max_length=60)
    link_to_photo: str = Field(..., max_length=200)
    description: Optional[str] = None

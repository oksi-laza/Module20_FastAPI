from backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Time, DateTime
from datetime import datetime
from sqlalchemy.sql import func


class Contact(Base):
    """A table for recording and storing contacts of a potential client: his name, phone number and email address."""
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String)
    privacy_policy_consent = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.name} {self.phone} {self.email}'


class MeetingAtOffice(Base):
    """
    A table containing information about the user's self-appointment for an office meeting at a convenient date and time
    """
    __tablename__ = 'meetings_at_office'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    date_of_meeting = Column(String(10), nullable=False)
    meeting_time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=func.now())
    privacy_policy_consent = Column(Boolean, default=True)

    def __str__(self):
        return f'{self.date_of_meeting} {self.meeting_time} {self.first_name} {self.last_name} - тел. {self.phone}'

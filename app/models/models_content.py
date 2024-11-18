from backend.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ServicesOffered(Base):
    """A table for working with information about the services provided by the company."""
    __tablename__ = 'services_offered'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False)
    link_to_photo = Column(String(200), nullable=False)

    foundations = relationship('Foundations', back_populates='service_offered', cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.title} {self.link_to_photo}'


class InfoGlavnoe(Base):
    """A table for working with information about the specifics of the company's work."""
    __tablename__ = 'info_glavnoe'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=False)

    def __str__(self):
        return self.title


class Foundations(Base):
    """A table for working with information about the foundations that the company is building."""
    __tablename__ = 'foundations'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False)
    link_to_photo = Column(String(200), nullable=False)
    description = Column(String)
    service_offered_id = Column(Integer, ForeignKey('services_offered.id'), nullable=False, index=True)

    service_offered = relationship('ServicesOffered', back_populates='foundations')

    def __str__(self):
        return f'{self.title} {self.link_to_photo}'

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from .base import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(String, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    street = Column(String)
    secret_hash = Column(String, nullable=False)
    records = relationship('Record', back_populates='device',
                           cascade='all, delete, delete-orphan')

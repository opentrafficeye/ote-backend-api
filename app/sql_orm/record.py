from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(),
                       nullable=False)
    vehicle_count = Column(Integer, nullable=False)
    delta = Column(Integer, nullable=False)
    device_id = Column(String, ForeignKey(
        'devices.id'), nullable=False, index=True)
    device = relationship('Device', back_populates='records')

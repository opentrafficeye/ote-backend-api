import datetime
from typing import List, Optional

from pydantic import BaseModel


class RecordBase(BaseModel):
    device_id: str
    vehicle_count: int
    delta: int


class RecordCreate(RecordBase):
    device_secret: str


class Record(RecordBase):
    timestamp: datetime.datetime
    id: int

    class Config:
        orm_mode = True


class Records(BaseModel):
    records: List[Record] = []

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    id: str
    latitude: Optional[float]
    longitude: Optional[float]
    street: Optional[str]


class DeviceCreate(DeviceBase):
    secret: str


class Device(DeviceBase):
    class Config:
        orm_mode = True


class Devices(BaseModel):
    devices: List[Device] = []

    class Config:
        orm_mode = True

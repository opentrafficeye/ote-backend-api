import datetime
from typing import List, Optional

import bcrypt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import schemas
from .sql_orm import Device, Record


def hash_secret(secret: str) -> str:
    """
    Hash secret.
    """
    return bcrypt.hashpw(
        secret.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def authenticate_device(session: Session, device_id: str, secret: str) -> bool:
    """
    Authenticate device.
    """
    db_device = session.query(Device).filter(
        Device.id == device_id
    ).first()
    if db_device is None:
        return False
    return bcrypt.checkpw(
        secret.encode('utf-8'), db_device.secret_hash.encode('utf-8'))


def get_devices(session: Session) -> List[Device]:
    """
    Get all devices from database.
    """
    return session.query(Device).all()


def get_records(
        session: Session,
        device_id: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        street: Optional[str] = None) -> list:
    """
    Get records from database.
    """
    q = session.query(Record)
    conditions = []
    if device_id is not None:
        conditions.append(Record.device_id == device_id)
    if start_time is not None:
        conditions.append(Record.timestamp >= start_time)
    if end_time is not None:
        conditions.append(Record.timestamp <= end_time)
    if street is not None:
        conditions.append(Device.street == street)
        q = q.join(Record.device)
    return q.filter(
        and_(*conditions)
    ).order_by(Record.timestamp.asc()).all()


def create_device(session: Session,
                  device: schemas.DeviceCreate) -> Device:
    """
    Create device in database.
    """
    db_device = Device(
        id=device.id,
        latitude=device.latitude,
        longitude=device.longitude,
        street=device.street,
        secret_hash=hash_secret(device.secret)
    )
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device


def create_record(session: Session,
                  record: schemas.RecordCreate) -> Optional[Record]:
    """
    Create record in database.
    """
    authorized = authenticate_device(
        session, record.device_id, record.device_secret)
    if not authorized:
        return None
    db_record = Record(vehicle_count=record.vehicle_count,
                       delta=record.delta,
                       device_id=record.device_id)
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

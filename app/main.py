import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .sql_orm import SessionLocal, init_db

app = FastAPI()
init_db()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get('/')
def read_root():
    return RedirectResponse(url='/docs')


@app.post('/devices', response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate,
                  session: Session = Depends(get_session)):
    db_device = crud.create_device(session, device)
    return db_device


@app.get('/devices/', response_model=schemas.Devices)
def read_device(session: Session = Depends(get_session)):
    db_devices = crud.get_devices(session)
    print(db_devices)
    return {'devices': db_devices}


@app.post('/records', response_model=schemas.Record)
def create_record(record: schemas.RecordCreate,
                  session: Session = Depends(get_session)):
    db_record = crud.create_record(session, record)
    if db_record is None:
        raise HTTPException(status_code=401, detail='Incorrect device secret')
    return db_record


@app.get('/records/', response_model=schemas.Records)
def read_record(device_id: Optional[str] = None,
                start_time: Optional[datetime.datetime] = None,
                end_time: Optional[datetime.datetime] = None,
                street: Optional[str] = None,
                session: Session = Depends(get_session)):
    db_records = crud.get_records(
        session, device_id, start_time, end_time, street)
    return {'records': db_records}

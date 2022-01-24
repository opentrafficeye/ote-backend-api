import time

from sqlalchemy.exc import OperationalError

from .base import Base


def init_db():
    for i in range(10):
        try:
            Base.metadata.create_all()
            break
        except OperationalError:
            time.sleep(i + 1)

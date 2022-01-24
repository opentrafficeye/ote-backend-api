from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = 'postgresql://postgres:postgres@postgres:5432/opentrafficeye'

engine = create_engine(db_string, client_encoding='utf8')
Base = declarative_base(engine)

SessionLocal = sessionmaker(engine)

import os
from sqlmodel import create_engine,SQLModel,Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql+psycopg2://postgres:12345@localhost:5432/FASQL'
engine = create_engine(DATABASE_URL,echo=True)#echo=True so we can see the generated SQL queries in the termina

def init_db():
    SQLModel.metadata.create_all(engine)

Base = declarative_base()

def get_session():
    with Session(engine) as session:
        yield session
from os import getenv
from typing import Any
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .models.db_model import Base

DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING")

if not DB_CONNECTION_STRING:
    raise Exception("DB connection string not provided")

engine = create_engine(DB_CONNECTION_STRING, echo=False, pool_pre_ping=True, pool_recycle=3600)
session_maker = sessionmaker(bind=engine, expire_on_commit=False)


def create_db() -> None:
    Base.metadata.create_all(engine)


def get_db() -> Generator[Session, Any, None]:
    with session_maker() as session:
        yield session


def auto_create_db():
    try:
        con = engine.connect()
        create_db()
        con.close()

    except Exception as _:
        connection_string, db_name = DB_CONNECTION_STRING.rsplit("/", 1)
        tmp_engine = create_engine(connection_string)

        raw_con = None
        try:
            raw_con = tmp_engine.raw_connection()

            raw_con.connection.set_session(autocommit=True)

            cursor = raw_con.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.close()
        finally:
            if raw_con:
                raw_con.close()

        create_db()

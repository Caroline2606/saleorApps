from sqlmodel import create_engine, SQLModel
from env.manage import FILE_NAME

SQLITE_FILE_NAME = FILE_NAME
sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """This def generates SQLModel engine
    for create database and tables"""

    SQLModel.metadata.create_all(engine)

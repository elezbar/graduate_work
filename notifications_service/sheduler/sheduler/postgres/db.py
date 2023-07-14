from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sheduler.core.config import db_url

Base = declarative_base()

engine = create_engine(db_url)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


def session(func):
    def wrapper(*args, **kwargs):
        wrapper.__annotations__ = func.__annotations__
        wrapper.__doc__ = func.__doc__
        with DBSession() as session:
            try:
                return func(*args, **kwargs, session=session)
            except Exception as e:
                session.rollback()
                raise e
    return wrapper

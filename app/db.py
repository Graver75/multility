from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DB(metaclass=SingletonMeta):
    def __init__(self, login, password, host, database):
        DATABASE_URL = f"mysql+pymysql://{login}:{password}@{host}/{database}"
        self.engine = create_engine(DATABASE_URL)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.Base = declarative_base()

    def get_session(self):
        return self.Session()

    def get_engine(self):
        return self.engine

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

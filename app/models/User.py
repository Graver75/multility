from sqlalchemy import Column, Integer, String, Text

from . import Base


class Module(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    name = Column(Text)
    role = Column(Text)

    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id

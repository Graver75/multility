from sqlalchemy import Column, Integer, String, Text

from app.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # Добавьте эту строку

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    name = Column(Text)
    role = Column(Text)

    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id

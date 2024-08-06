from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Note(Base):
    __tablename__ = 'notes'
    __table_args__ = {'extend_existing': True}  # Добавьте эту строку

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    type = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

    def __init__(self, title, type, content, user_id):
        self.title = title
        self.type = type
        self.content = content
        self.user_id = user_id

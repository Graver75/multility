from sqlalchemy import Column, Integer, String, Text

from . import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

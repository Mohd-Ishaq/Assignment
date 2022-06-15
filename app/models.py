from sqlalchemy import Column, Integer, String
from .database import Base


""" All users credentials and message will store in Data_Table """


class Data_Table(Base):
    __tablename__ = "data_table"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    message = Column(String, nullable=False)

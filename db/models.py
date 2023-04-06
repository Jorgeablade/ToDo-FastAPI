from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
import datetime
from db import Base
 
class Todo(Base):
    __tablename__ = "todos"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    complete = Column(Boolean, default=False)
    # auto add date, but just, year, month, day
    date = Column(DateTime, default=datetime.datetime.now().date())

class user(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import app


class User:
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    course = Column(String, nullable=False)


class Course:
    __tablename__ = "course"

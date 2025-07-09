from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import os
from app import app

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"


class Student(db.Model):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)


class Course(db.Model):
    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String, unique=True, nullable=False)
    course_name = Column(String, nullable=False)
    course_description = Column(String)


class Enrollments(db.Model):
    __tablename__ = "enrollments"
    eenrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    estudent_id = Column(Integer, ForeignKey("student.student_id"), nullable=False)
    ecourse_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)


db.init_app(app=app)
app.app_context().push()


if not os.path.exists("/instance/database.sqlite3"):
    print("Database not Found Creating It")
    db.create_all()

    courses = [
        Course(
            course_code="CSE01",
            course_name="MAD 1",
            course_description="Modern Application Development - I",
        ),
        Course(
            course_code="CSE02",
            course_name="DBMS",
            course_description="Database management Systems",
        ),
        Course(
            course_code="CSE03",
            course_name="PDSA",
            course_description="Programming, Data Structures and Algorithms using Python",
        ),
        Course(
            course_code="BST13",
            course_name="BDM",
            course_description="Business Data Management",
        ),
    ]

    db.session.add_all(courses)
    db.session.commit()

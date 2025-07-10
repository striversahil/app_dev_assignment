from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


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
    course_id = Column(String, primary_key=True)
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


if not os.path.exists("instance/database.sqlite3"):
    print("Database not Found Creating It")
    db.create_all()

    courses = [
        Course(
            course_id="CSE01",
            course_code="CSE01",
            course_name="MAD 1",
            course_description="Modern Application Development - I",
        ),
        Course(
            course_id="CSE02",
            course_code="CSE02",
            course_name="DBMS",
            course_description="Database management Systems",
        ),
        Course(
            course_id="CSE03",
            course_code="CSE03",
            course_name="PDSA",
            course_description="Programming, Data Structures and Algorithms using Python",
        ),
        Course(
            course_id="BST13",
            course_code="BST13",
            course_name="BDM",
            course_description="Business Data Management",
        ),
    ]

    db.session.add_all(courses)
    db.session.commit()


@app.route("/student/create", methods=["GET", "POST"])
def addstudent():
    if request.method == "POST":
        roll = request.form.get("roll")
        first = request.form.get("first")
        last = request.form.get("last")
        courses = request.form.getlist("course")
        if not roll or not first or not last or not courses:
            return redirect(url_for("home"))

        already = Student.query.filter_by(roll_number=roll).first()
        if already:
            return render_template("addstudent.html", already=True)

        student = Student(roll_number=roll, first_name=first, last_name=last)
        db.session.add(student)
        db.session.commit()

        for course in courses:
            enrollment = Enrollments(estudent_id=student.student_id, ecourse_id=course)
            db.session.add(enrollment)
            db.session.commit()

        return redirect(url_for("home"))

    return render_template("addstudent.html")


@app.route("/student/<int:studentId>/update", methods=["GET", "POST"])
def update(studentId):
    student = Student.query.filter_by(student_id=studentId).first()
    if not student:
        return redirect(url_for("home"))

    if request.method == "POST":
        roll = request.form.get("roll")
        first = request.form.get("first")
        last = request.form.get("last")
        courses = request.form.getlist("course")
        if not roll or not first or not last or not courses:
            return redirect(url_for("home"))
        student.roll_number = roll
        student.first_name = first
        student.last_name = last
        db.session.commit()

    print(student)
    return render_template("addstudent.html", student=student)


@app.route("/", methods=["GET", "POST"])
def home():
    students = Student.query.all()

    return render_template("home.html", students=students)


if __name__ == "__main__":
    app.run()

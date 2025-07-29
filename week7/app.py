from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///week7_database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)


class Course(db.Model):
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False)
    course_code = Column(String(20), unique=True, nullable=False)
    course_description = Column(String(255), nullable=True)


class Enrollment(db.Model):
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    estudent_id = Column(Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = Column(Integer, db.ForeignKey("course.course_id"), nullable=False)

    student = db.relationship("Student", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/courses", methods=["GET"])
def courses():
    # This route would display a list of all courses
    # If no courses exist, it would return an empty list or a message
    courses = Course.query.all()
    return render_template("courses.html", courses=courses)


@app.route("/courses/create", methods=["GET", "POST"])
def create_course():
    # This route would handle the creation of a new course
    # If course exists, it would return an error message
    return render_template("create_course.html")


@app.route("/courses/<int:course_id>", methods=["GET"])
def course_detail(course_id):
    # This route would display the details of a specific course along with its enrolled students
    # If course does not exist, it would return an error message
    course = Course.query.get(course_id)
    if course:
        return render_template("course_detail.html", course=course)
    else:
        return "Course not found", 404


@app.route("/courses/<int:course_id>/update", methods=["GET", "POST"])
def update_course(course_id):
    # This route would handle updating an existing course's information
    # If course does not exist, it would return an error message
    return render_template("update_course.html", course_id=course_id)


@app.route("/students/create", methods=["GET", "POST"])
def create_student():
    # This route would handle the creation of a new student
    # If student exists, it would return an error message
    return render_template("create_student.html")


@app.route("/students/<int:student_id>", methods=["GET"])
def student_detail(student_id):
    # This route would display the details of a specific student
    # If student does not exist, it would return an error message
    student = Student.query.get(student_id)
    if student:
        return render_template("student_detail.html", student=student)
    else:
        return "Student not found", 404


@app.route("/students/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
    # This route would handle updating an existing student's information
    # If student does not exist, it would return an error message
    return render_template("update_student.html", student_id=student_id)


with app.app_context():
    if not os.path.exists("week7_database.sqlite3"):
        print("Creating the database...")
        db.create_all()
        print("Database created successfully.")


if __name__ == "__main__":
    app.run(debug=True)

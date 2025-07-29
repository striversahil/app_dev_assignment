from flask import Flask, render_template, request, redirect, url_for
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
    course_code = Column(String(20), unique=True, nullable=False)
    course_name = Column(String(100), nullable=False)
    course_description = Column(String(255), nullable=True)


class Enrollment(db.Model):
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    estudent_id = Column(Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = Column(Integer, db.ForeignKey("course.course_id"), nullable=False)

    student = db.relationship("Student", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")


@app.route("/", methods=["GET"])
def index():
    # It will render all student or Add a student and go to the courses page
    students = Student.query.all()
    return render_template("index.html", students=students), 200


@app.route("/courses", methods=["GET"])
def courses():
    # This route would display a list of all courses
    # If no courses exist, it would return an empty list or a message
    courses = Course.query.all()
    return render_template("courses.html", courses=courses), 200


@app.route("/course/create", methods=["GET", "POST"])
def create_course():
    if request.method == "POST":
        course_name = request.form.get("c_name")
        course_code = request.form.get("code")
        course_description = request.form.get("desc")

        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course:
            return render_template(
                "create_course.html", error="Course with this code already exists."
            )

        new_course = Course(
            course_name=course_name,
            course_code=course_code,
            course_description=course_description,
        )
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("courses"))
    # This route would handle the creation of a new course
    # If course exists, it would return an error message
    return render_template("create_course.html"), 200


@app.route("/course/<int:course_id>/delete", methods=["GET"])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        enrollments = Enrollment.query.filter_by(ecourse_id=course_id).all()
        for enrollment in enrollments:
            db.session.delete(enrollment)
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for("courses"))
    else:
        return "Course not found", 404


@app.route("/course/<int:course_id>", methods=["GET"])
def course_detail(course_id):
    # This route would display the details of a specific course along with its enrolled students
    # If course does not exist, it would return an error message
    course = Course.query.get(course_id)
    students = (
        Student.query.join(Enrollment).filter(Enrollment.ecourse_id == course_id).all()
    )
    if course:
        return (
            render_template("course_detail.html", course=course, students=students),
            200,
        )
    else:
        return render_template("course_detail.html", error="Course not found."), 404


@app.route("/course/<int:course_id>/update", methods=["GET", "POST"])
def update_course(course_id):
    # This route would handle updating an existing course's information
    # If course does not exist, it would return an error message
    course = Course.query.get(course_id)
    if request.method == "POST":
        if not course:
            return render_template("update_course.html", error="Course not found.")

        course.course_name = request.form.get("c_name")
        course.course_description = request.form.get("desc")

        db.session.commit()
        return redirect(url_for("courses"))
    return render_template("update_course.html", course=course), 200


@app.route("/student/create", methods=["GET", "POST"])
def create_student():
    # This route would handle the creation of a new student
    # If student exists, it would return an error message
    if request.method == "POST":
        roll_number = request.form.get("roll")
        first_name = request.form.get("f_name")
        last_name = request.form.get("l_name")

        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            return (
                render_template(
                    "create_student.html",
                    error="Student with this roll number already exists.",
                ),
                200,
            )

        new_student = Student(
            roll_number=roll_number, first_name=first_name, last_name=last_name
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for("index")), 201
    return render_template("create_student.html")


@app.route("/student/<int:student_id>/delete", methods=["GET"])
def delete_student(student_id):
    # This route would handle the deletion of a student
    # If student does not exist, it would return an error message
    student = Student.query.get(student_id)
    if student:
        enrollment = Enrollment.query.filter_by(estudent_id=student_id).first()
        if enrollment:
            db.session.delete(enrollment)
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return "Student not found", 404


@app.route("/student/<int:student_id>", methods=["GET"])
def student_detail(student_id):
    # This route would display the details of a specific student
    # If student does not exist, it would return an error message
    student = Student.query.get(student_id)
    courses = (
        Course.query.join(Enrollment).filter(Enrollment.estudent_id == student_id).all()
    )

    if student:
        return (
            render_template("student_detail.html", student=student, courses=courses),
            200,
        )
    else:
        return "Student not found", 404


@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
    # This route would handle updating an existing student's information
    # If student does not exist, it would return an error message
    courses = Course.query.all()
    student = Student.query.get(student_id)
    if request.method == "POST":
        enrollment = Enrollment.query.filter_by(estudent_id=student_id).first()
        if not student:
            return (
                render_template("update_student.html", error="Student not found."),
                404,
            )

        student.first_name = request.form.get("f_name")
        student.last_name = request.form.get("l_name")
        if enrollment:
            enrollment.ecourse_id = int(request.form.get("course"))
        else:
            new_enrollment = Enrollment(
                estudent_id=student_id, ecourse_id=int(request.form.get("course"))
            )
            db.session.add(new_enrollment)

        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update_student.html", student=student, courses=courses), 200


@app.route("/student/<int:student_id>/withdraw/<int:course_id>", methods=["GET"])
def withdraw_student(student_id, course_id):
    enrollment = Enrollment.query.filter_by(
        estudent_id=student_id, ecourse_id=course_id
    ).first()
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        return redirect(url_for("student_detail", student_id=student_id))
    else:
        return "Enrollment not found", 404


if __name__ == "__main__":
    app.run(debug=True)

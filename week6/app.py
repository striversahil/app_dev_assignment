from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api_database.sqlite3"
db = SQLAlchemy()


class Course(db.Model):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(50), nullable=False)
    course_code = Column(String(200), unique=True, nullable=False)
    course_description = Column(String(500), nullable=True)


class Student(db.Model):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(ForeignKey("students.student_id"), nullable=False)
    course_id = Column(ForeignKey("courses.course_id"), nullable=False)

    student = db.relationship("Student", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")


@app.route("/")
def home():
    return "Welcome to the Page!"


@app.route("/api/course/<course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return {"error": "Course not found"}, 404
    return {
        "course_id": course.course_id,
        "course_name": course.course_name,
        "course_code": course.course_code,
        "course_description": course.course_description
    } , 200

@app.route("/api/course/<course_id>", methods=["PUT"])
def update_course(course_id):
    course_name = request.json.get("course_name")
    course_code = request.json.get("course_code")
    course_description = request.json.get("course_description")

    if not course_name :
        return {"error_code" : "COURSE001" , "error_message" : "Course name is required"}, 400

    if not course_code:
        return {"error_code" : "COURSE002" , "error_message" : "Course code is required"}, 400

    course = Course.query.get(int(course_id))
    if course is None:
        return {"error": "Course not found"}, 404
    course.course_name = course_name
    course.course_code = course_code
    course.course_description = course_description
    db.session.commit()
    return {"message": "Course updated successfully"} , 200

@app.route("/api/course/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get(int(course_id))
    if course is None:
        return "Course not found", 404
    db.session.delete(course)
    db.session.commit()
    return "Successfully Deleted", 200


@app.route("/api/course", methods=["POST"])
def create_course():
    course_name = request.json.get("course_name")
    course_code = request.json.get("course_code")
    course_description = request.json.get("course_description")

    course = Course.query.filter_by(course_code=course_code).first()
    if course:
        return "course_code already exist", 409
    
    if not course_name :
        return {"error_code" : "COURSE001" , "error_message" : "Course name is required"}, 400

    if not course_code:
        return {"error_code" : "COURSE002" , "error_message" : "Course code is required"}, 400
    
    new_course = Course(
        course_name=course_name,
        course_code=course_code,
        course_description=course_description
    )
    db.session.add(new_course)
    db.session.commit()
    return "Successfully Created", 201


@app.route("/api/student/<student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return "Student not found", 404
    return {
        "student_id": student.student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "roll_number": student.roll_number
    } , 200


@app.route("/api/student/<student_id>", methods=["PUT"])
def update_student(student_id):
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    roll_number = request.json.get("roll_number")

    if not roll_number:
        return {"error_code": "STUDENT001", "error_message": "Roll number required"}, 400
    
    if not first_name:
        return {"error_code": "STUDENT002", "error_message": "First name required"}, 400
    
    student = Student.query.get(int(student_id))
    if student is None:
        return "Student not found", 404
    return {
        "student_id": student.student_id,
        "first_name": first_name,
        "last_name": last_name,
        "roll_number": roll_number
    } , 200


@app.route("/api/student/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(int(student_id))
    if student is None:
        return "Student not found", 404
    db.session.delete(student)
    db.session.commit()
    return "Successfully Deleted", 200


@app.route("/api/student", methods=["POST"])
def create_student():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    roll_number = request.json.get("roll_number")

    print(request.json)

    student = Student.query.filter_by(roll_number=roll_number).first()
    if student:
        return "Student already exists", 409

    if not roll_number:
        return {"error_code": "STUDENT001", "error_message": "Roll number required"}, 400
    
    if not first_name:
        return {"error_code": "STUDENT002", "error_message": "First name required"}, 400
    
    new_student = Student(
        first_name=first_name,
        last_name=last_name,
        roll_number=roll_number
    )
    db.session.add(new_student)
    db.session.commit()
    return "Successfully Created", 201

@app.route("/api/student/<student_id>/course", methods=["GET"])
def get_student_courses(student_id):
    student = Student.query.get(int(student_id))
    if student is None:
        return {"error_code" : "ENROLLMENT002" , "error_message": "Student does not exist"}, 404

    enrolled_courses = Enrollment.query.filter_by(student_id=student_id).all()
    if not enrolled_courses:
        return "Student is not enrolled in any course", 404

    return enrolled_courses, 200

@app.route("/api/student/<student_id>/course", methods=["POST"])
def enroll_student_in_course(student_id):
    course_id = request.json.get("course_id")
    if not course_id:
        return {"error_code": "ENROLLMENT001", "error_message": "Course does not exist"}, 400
    new_enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )
    db.session.add(new_enrollment)
    db.session.commit()
    return "Enrollment successful", 201

@app.route("/api/student/<student_id>/course/<course_id>", methods=["DELETE"])
def unenroll_student_from_course(student_id, course_id):
    if not course_id:
        return {"error_code": "ENROLLMENT001", "error_message": "Course does not exist"}, 400
    
    if not student_id:
        return {"error_code": "ENROLLMENT002", "error_message": "Student does not exist"}, 400

    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if enrollment is None:
        return "Enrollment for the student not found", 404
    db.session.delete(enrollment)
    db.session.commit()
    return "Successfully deleted", 200


db.init_app(app)


if not os.path.exists("instance/api_database.sqlite3"):
    print("Database file does not exist. Creating a new one...")
    with app.app_context():
        db.create_all()

def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()



# curl -X POST http://localhost:5000/api/student -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "roll_number": "12345"}'
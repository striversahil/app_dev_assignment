from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import matplotlib.pyplot as plt
from collections import Counter

app = Flask(__name__)


def course(course_id: str) -> dict:
    data = get_data()
    course_records = []
    course = {"average_marks": 0, "maximum_marks": 0}
    for record in data:
        if record[1].strip() == course_id:
            course_records.append(record)
    if not course_records:
        return {}
    total_marks = sum(int(record[2]) for record in course_records)
    course["average_marks"] = total_marks / len(course_records)
    course["maximum_marks"] = max(int(record[2]) for record in course_records)

    # Plotting the course marks
    each_marks = sorted(int(record[2]) for record in course_records)
    frequency = Counter(each_marks)
    plt.figure(figsize=(10, 5))
    plt.bar(frequency.keys(), height=frequency.values(), width=4, color="b")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig("static/course.png")

    return course


def student(student_id: str) -> tuple:
    data = get_data()
    student_records = []
    for record in data:
        if record[0].strip() == student_id:
            student_records.append(record)
    total_marks = sum(int(record[2]) for record in student_records)
    return student_records, total_marks


def get_data() -> list:

    try:
        with open("data.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            return data
    except Exception as e:
        return []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        course_id = request.form.get("course_id")
        student_id = request.form.get("student_id")
        value = request.form.get("value")

        if not value:
            return render_template("index.html", error="Wrong Inputs")

        if student_id:
            student_records, total_marks = student(value)
            if not student_records:
                return render_template("index.html", error="Wrong Inputs")

            return render_template(
                "index.html", studentDetails=student_records, totalMarks=total_marks
            )
        if course_id:
            course_details = course(value)
            if not course_details:
                return render_template("index.html", error="Wrong Inputs")

            return render_template(
                "index.html",
                courseDetails=course_details,
            )

        return render_template(
            "index.html", course_id=course_id, student_id=student_id, value=value
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

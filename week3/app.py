import sys
import csv
import os
from jinja2 import Template
import matplotlib.pyplot as plt
from collections import Counter


errorTemplate = Template(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
</head>
<body>
    <h1>Wrong Input</h1>
    <p>Something went wrong</p>
</body>
</html>
"""
)


studentTemplate = Template(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Details</title>
</head>
<body>
    <h1>Student Details</h1>

    <table border="2">
        <tr>
            <th>Student id</th>
            <th>Course id</th>
            <th>Marks</th>
        </tr>
    {% for student in students %}
        <tr>
            <td>{{ student[0] }}</td>
            <td>{{ student[1] }}</td>
            <td>{{ student[2] }}</td>
        </tr>
    {% endfor %}
        <tr>
            <td colspan="2"> Total Marks</td>
            <td>{{ total_marks }}</td>
        </tr>
    </table>
</body>
</html>
"""
)


courseTemplate = Template(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Details</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="2">
        <tr>
            <td>Average Marks</td>
            <td>Maximum Marks</td>
        </tr>
        <tr>
            <td>{{ average }}</td>
            <td> {{ maximum }}</td>
        </tr>
    </table>
    <image src="course.png" alt="Course Image">
</body>
</html>

"""
)


def readCSV():
    try:
        if os.path.exists("data.csv"):
            with open("data.csv", "r") as file:
                reader = csv.reader(file)
                data = list(reader)
                return data
        else:
            return []
    except Exception as e:
        return []


def courseFunction(course_id: str):
    if int(course_id) <= 0:
        errorFunction()

    each_marks = []
    max_marks = 0

    for rows in readCSV():
        if rows[1].strip() == course_id:
            each_marks.append(int(rows[2]))
            max_marks = max(int(max_marks), int(rows[2]))

    if not each_marks:
        return "error"

    # Plotting the course marks
    each_marks = sorted(each_marks)
    frequency = Counter(each_marks)
    plt.figure(figsize=(10, 5))
    plt.bar(frequency.keys(), height=frequency.values(), width=4, color="b")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")

    plt.savefig("course.png")
    avg_marks = round(sum(each_marks) / len(each_marks), 1)

    output = courseTemplate.render(average=avg_marks, maximum=max_marks)
    with open("output.html", "w") as file:
        file.write(output)
    return "success"


def studentFunction(student_id: str):
    if int(student_id) <= 0:
        return "error"
    students = []
    total_marks = 0

    for rows in readCSV():
        if rows[0].strip() == student_id:
            students.append(rows)
            total_marks = total_marks + int(rows[2])

    if not students:
        return "error"

    output = studentTemplate.render(students=students, total_marks=total_marks)
    with open("output.html", "w") as file:
        file.write(output)

    return "success"


def errorFunction():
    error = errorTemplate.render()
    with open("output.html", "w") as file:
        file.write(error)


def main():
    print("Welcome to Course and Student Analysis !")

    status = ""

    if len(sys.argv) != 3:
        status = "error"

    if sys.argv[1] not in ["-s", "-c"]:
        status = "error"

    if sys.argv[1] == "-s":
        output = studentFunction(sys.argv[2])
        status = output

    elif sys.argv[1] == "-c":
        output = courseFunction(sys.argv[2])
        status = output

    if status == "error":
        errorFunction()


if __name__ == "__main__":
    main()

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import re

app = FastAPI()

students = []


class Student(BaseModel):
    name: str
    email: str
    age: int
    courses: list[str]


class StudentEmail(BaseModel):
    email: str


# Get Student Information
@app.get("/students/{student_id}")
def get_student(student_id: int, include_grades: bool, semester: Optional[str] = None):
    try:
        if student_id <= 1000:
            raise ValueError("Student ID should be greater than 1000")
        if student_id > 9999:
            raise ValueError("Student ID should be less than 9999")
        if not isinstance(include_grades, bool):
            raise ValueError("Include Grades should be a boolean")
        if semester:
            if not re.match(r"^(Fall|Spring|Summer)\d{4}$", semester):
                raise ValueError("Invalid Semester Format")

        # Get Student Information
        student = filter(lambda x: x["student_id"] == student_id, students)
        student = list(student)
        if not student:
            raise ValueError("Student not found")
        student = student[0]

        return {"status": "success", "data": student}
    except Exception as e:
        return {"message": str(e), "status": "error", "data": None}


# Register Student
@app.post("/students/register")
def register_student(student: Student):
    try:
        if not re.match(r"^[a-zA-Z ]{1,50}$", student.name):
            raise ValueError("Invalid Name")
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", student.email
        ):
            raise ValueError("Invalid Email")
        if any(x["email"] == student.email for x in students):
            raise ValueError("Email already exists")
        if student.age < 18 or student.age > 30:
            raise ValueError("Invalid Age")
        if len(student.courses) < 1 or len(student.courses) > 5:
            raise ValueError("Invalid Courses")
        if len(set(student.courses)) != len(student.courses):
            raise ValueError("Duplicate Courses")
        for course in student.courses:
            if not re.match(r"^[a-zA-Z ]{5,30}$", course):
                raise ValueError("Invalid Course Name")

        students.append(
            {
                "student_id": 1000 + len(students) + 1,
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "courses": student.courses,
            }
        )

        return {"status": "success", "data": students[len(students) - 1]}
    except Exception as e:
        return {"message": str(e), "status": "error", "data": None}


@app.put("/students/{student_id}/email")
def update_student_email(student_id: int, body: StudentEmail):
    print("body", body)
    email = body.email
    try:
        if student_id <= 1000:
            raise ValueError("Student ID should be greater than 1000")
        if student_id > 9999:
            raise ValueError("Student ID should be less than 9999")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Invalid Email")
        if any(x["email"] == email for x in students if x["student_id"] != student_id):
            raise ValueError("Email already exists")
        student = filter(lambda x: x["student_id"] == student_id, students)
        student = list(student)
        if not student:
            raise ValueError("Student not found")
        student = student[0]

        student["email"] = email

        return {"status": "success", "data": student}
    except Exception as e:
        return {"message": str(e), "status": "error", "data": None}

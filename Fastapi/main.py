from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()
# http://127.0.0.1:8000
students = []

class Student(BaseModel):
    id: str 
    name : str
    lastname : str 
    skills : List[str] = []

@app.get("/students")
def get_students():
    return students

@app.get("/students/{id}")
def get_students(id: str):
    for student in students:
        if student["id"] == id:
            return student
    return "No existe el estudiante"


@app.post("/students")
def save_student(student: Student):
    student.id = str(uuid4())
    students.append(student.dict())
    return f'Estudiante guardado'

@app.put("/students/{id}")
def update_student(update_student : Student, id:str):
    for student in students:
        if student["id"] == id:
            student["name"] = update_student.name
            student["lastname"] = update_student.lastname
            student["skills"] = update_student.skills
            return f'Estudiante modificado'
    return "No existe el estudiante"

@app.delete("/students/{id}")
def delete_student(id:str):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            return 'Estudiante eliminado'
    return 'No existe el estudiante'

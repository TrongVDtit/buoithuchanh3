from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Load accounts from file
def load_accounts():
    accounts = {}
    if os.path.exists('accounts.txt'):
        with open('accounts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                user, password = line.strip().split(',')
                accounts[user] = password
    return accounts

accounts = load_accounts()

# Student model and load students from file
class Student(BaseModel):
    id: int
    name: str
    age: int
    address: str
    phone: str
    email: str
    class_name: str

def load_students():
    students = []
    if os.path.exists('students.txt'):
        with open('students.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split(',')
                student = Student(
                    id=int(data[0]),
                    name=data[1],
                    age=int(data[2]),
                    address=data[3],
                    phone=data[4],
                    email=data[5],
                    class_name=data[6]
                )
                students.append(student)
    return students

students = load_students()

def save_students(students: List[Student]):
    with open('students.txt', 'w', encoding='utf-8') as f:
        for student in students:
            f.write(f"{student.id},{student.name},{student.age},{student.address},{student.phone},{student.email},{student.class_name}\n")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("login.html")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in accounts and accounts[username] == password:
        return RedirectResponse(url="/admin", status_code=303)
    else:
        return HTMLResponse(content="Tài khoản hoặc mật khẩu không chính xác", status_code=400)

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    return FileResponse("admin.html")

@app.get("/students", response_model=List[Student])
async def get_students():
    return students

@app.post("/students", response_model=Student)
async def add_student(name: str = Form(...), age: int = Form(...), address: str = Form(...), phone: str = Form(...), email: str = Form(...), class_name: str = Form(...)):
    student_id = len(students) + 1
    student = Student(id=student_id, name=name, age=age, address=address, phone=phone, email=email, class_name=class_name)
    students.append(student)
    save_students(students)
    return student

# Run the app with: uvicorn main:app --reload

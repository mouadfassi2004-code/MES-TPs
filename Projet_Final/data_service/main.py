from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import (
    init_database,
    get_student_by_credentials,
    get_students,
    get_professors,
    get_modules,
    get_planning,
    get_exams,
    get_announcements,
    get_general_info
)

app = FastAPI(
    title="CampusBot Data Service",
    description="Service de données CampusBot avec SQLite",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


@app.on_event("startup")
def startup_event():
    init_database(reset=False)


@app.get("/")
def home():
    return {
        "service": "CampusBot Data Service",
        "status": "running",
        "database": "SQLite",
        "version": "3.0.0"
    }


@app.post("/api/login")
def login(request: LoginRequest):
    student = get_student_by_credentials(request.email, request.password)

    if not student:
        return {
            "success": False,
            "message": "Email ou mot de passe incorrect."
        }

    return {
        "success": True,
        "message": "Connexion réussie.",
        "student": student
    }


@app.get("/api/all")
def get_all_data():
    modules = get_modules()
    professors = get_professors()
    planning = get_planning()
    exams = get_exams()
    announcements = get_announcements()
    general_info = get_general_info()

    return {
        "project": {
            "name": "CampusBot",
            "university": "Université Euromed de Fès",
            "target": "Étudiants de l'Université Euromed de Fès",
            "objective": "Faciliter l'accès aux informations universitaires, surtout pendant la période des examens.",
            "supervisor": "AMAMOU Ahmed",
            "students": [
                "Mouad Fassi Fihri",
                "Benlhabib Mohamed El Ghali"
            ]
        },
        "university": {
            "name": "Université Euromed de Fès",
            "department": "Big Data",
            "level": "1ère année Big Data",
            "academic_year": "2025/2026"
        },
        "students": get_students(),
        "modules": modules,
        "professors": professors,
        "planning": planning,
        "schedule": [
            {
                "day": item["day"],
                "time": item["time"],
                "module_id": item["module"],
                "professor": item["professor"],
                "room": item["room"],
                "group_name": item["group_name"],
                "session_type": item["session_type"]
            }
            for item in planning
        ],
        "exams": exams,
        "announcements": announcements,
        "general_info": general_info
    }


@app.get("/api/students")
def api_students():
    return get_students()


@app.get("/api/modules")
def api_modules():
    return get_modules()


@app.get("/api/professors")
def api_professors():
    return get_professors()


@app.get("/api/planning")
def api_planning():
    return get_planning()


@app.get("/api/schedule")
def api_schedule():
    return get_planning()


@app.get("/api/exams")
def api_exams():
    return get_exams()


@app.get("/api/announcements")
def api_announcements():
    return get_announcements()


@app.get("/api/general-info")
def api_general_info():
    return get_general_info()
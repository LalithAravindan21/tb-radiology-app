from fastapi import FastAPI, Form, UploadFile, File, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
import shutil
import requests
import os
import json

app = FastAPI()

# Set your Google API key here
GOOGLE_API_KEY = "AIzaSyDTnW0BTElejIsvEk0ylSjmmrFT7nSIT48"

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

patients = {}

def dummy_tb_predict(file_path):
    from random import uniform
    return round(uniform(0.0, 1.0), 2)  # Simulated percentage

def generate_google_ai_report(score, name, age, gender):
    prompt = f"""
    Generate a professional radiology report based on the following information:

    Patient: {name}, Age: {age}, Gender: {gender}
    TB Detection Confidence: {score * 100:.2f}%

    Provide:
    - Severity level
    - Medical explanation
    - Suggested next steps for treatment or further diagnosis
    """

    url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": {"text": prompt},
        "temperature": 0.7,
        "candidateCount": 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["output"]
    else:
        return f"Error generating report: {response.text}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_b64": None,
        "report": None,
        "message": None
    })

@app.post("/register/")
async def register_patient(
    request: Request,
    patient_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...)
):
    patients[patient_id] = {
        "name": name,
        "age": age,
        "gender": gender
    }
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"Patient {name} registered successfully.",
        "image_b64": None,
        "report": None
    })

@app.post("/predict/")
async def predict(
    request: Request,
    patient_id: str = Form(...),
    file: UploadFile = File(...)
):
    if patient_id not in patients:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"Patient ID {patient_id} not found.",
            "image_b64": None,
            "report": None
        })

    file_path = f"static/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Simulate prediction
    score = dummy_tb_predict(file_path)

    # Get patient details
    patient = patients[patient_id]
    name = patient["name"]
    age = patient["age"]
    gender = patient["gender"]

    # Get AI-generated report
    report_text = generate_google_ai_report(score, name, age, gender)

    with open(file_path, "rb") as img:
        image_b64 = base64.b64encode(img.read()).decode()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"X-ray analyzed for patient {patient_id}.",
        "image_b64": image_b64,
        "report": report_text
    })

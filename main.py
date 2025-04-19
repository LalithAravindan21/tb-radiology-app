from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import base64
import random

app = FastAPI()

# Mount static and templates folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Allow CORS (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TB Prediction Logic
def predict_tb(file, name, age, gender, date):
    image = Image.open(file.file)

    # Simulated severity score
    severity = round(random.uniform(0.0, 1.0), 2)

    # Condition & Recommendation based on severity
    if severity < 0.3:
        condition = "Normal"
        recommendation = "No TB detected"
    elif severity < 0.6:
        condition = "Mild"
        recommendation = "Recommend monitoring and follow-up"
    elif severity < 0.85:
        condition = "Moderate"
        recommendation = "Suggest detailed testing"
    else:
        condition = "Severe"
        recommendation = "Urgent care and treatment needed"

    report = {
        "condition": condition,
        "recommendation": recommendation,
        "accuracy": f"{severity * 100:.2f}%"
    }

    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return image_b64, severity, report


# Root page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Prediction route
@app.post("/predict/", response_class=HTMLResponse)
async def predict(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    date: str = Form(...)
):
    image_b64, severity, report = predict_tb(file, name, age, gender, date)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "image": image_b64,
        "report": report,
        "severity": f"{severity * 100:.2f}%",
        "patient_id": name,
        "age": age,
        "gender": gender
    })

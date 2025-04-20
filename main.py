from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime

app = FastAPI()

# Ensure static/uploads folder exists
os.makedirs("static/uploads", exist_ok=True)

# Mount static files (to serve index.html and assets)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/predict/")
async def predict(
    file: UploadFile = File(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    date: str = Form(...)
):
    try:
        # Save uploaded image
        filename = file.filename
        file_path = f"static/uploads/{filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Dummy prediction logic — replace with model inference
        disease_probability = 0.78  # Example: 78% TB
        severity = (
            "Mild" if disease_probability < 0.5 else
            "Moderate" if disease_probability < 0.8 else
            "Severe"
        )
        recommendation = (
            "Routine follow-up" if severity == "Mild" else
            "Schedule further tests" if severity == "Moderate" else
            "Immediate medical attention required"
        )

        # Dummy Google API logic placeholder (you would use the API key here if needed)
        # Example: query medical articles based on severity, condition, etc.

        report = {
            "name": name,
            "age": age,
            "gender": gender,
            "date": date,
            "image_url": f"/static/uploads/{filename}",
            "disease_probability": f"{disease_probability*100:.2f}%",
            "severity": severity,
            "recommendation": recommendation
        }

        return JSONResponse(content=report)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

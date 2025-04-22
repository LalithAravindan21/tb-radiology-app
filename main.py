from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure static/uploads folder exists
os.makedirs("static/uploads", exist_ok=True)

# Mount static files (to serve index.html and assets)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint to check the status
@app.get("/")
def read_root():
    return {"status": "OK", "message": "TB X‑Ray API is running"}

# Endpoint to serve the index.html for uploading files
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("static/index.html", "r") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

# Endpoint to handle file uploads and predictions
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

        # Dummy prediction logic — replace with real model inference
        disease_probability = 0.78  # Just a placeholder

        # Determine severity
        severity = (
            "Mild" if disease_probability < 0.5 else
            "Moderate" if disease_probability < 0.8 else
            "Severe"
        )

        # Recommendation based on severity
        recommendation = (
            "Routine follow-up" if severity == "Mild" else
            "Schedule further tests" if severity == "Moderate" else
            "Immediate medical attention required"
        )

        # Dummy report — can be extended with Google API call if needed
        report = {
            "name": name,
            "age": age,
            "gender": gender,
            "date": date,
            "image_url": f"/static/uploads/{filename}",
            "disease_probability": f"{disease_probability * 100:.2f}%",
            "severity": severity,
            "recommendation": recommendation
        }

        return JSONResponse(content=report)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

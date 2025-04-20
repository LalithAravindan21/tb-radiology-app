from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/register/")
async def register_patient(id: str = Form(...), name: str = Form(...), age: int = Form(...), gender: str = Form(...)):
    # You can store the patient in a DB if needed
    return {"message": "Patient registered successfully"}

@app.post("/predict/", response_class=HTMLResponse)
async def predict(file: UploadFile = File(...), patient_id: str = Form(...)):
    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Fake inference & report for now
    # You can replace this with actual model + GPT
    severity = "Moderate"
    accuracy = 87.3

    html = f"""
        <h3>AI Report</h3>
        <p><strong>Condition:</strong> {severity} TB detected</p>
        <p><strong>Accuracy:</strong> {accuracy:.2f}%</p>
        <p><strong>Recommendation:</strong> Immediate clinical follow-up suggested.</p>
    """
    return HTMLResponse(content=html)

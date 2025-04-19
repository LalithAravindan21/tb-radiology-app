from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model_utils import process_image_and_generate_report
from patient_store import save_patient, load_patient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict/")
async def predict(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    date: str = Form(...)
):
    image_b64, report = process_image_and_generate_report(file, name, age, gender, date)
    save_patient(name, age, gender, date, report)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image": image_b64,
        "report": report
    })

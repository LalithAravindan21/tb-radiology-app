from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
from io import BytesIO
from model_utils import predict_tb  # Your model logic for prediction

app = FastAPI()

# Serving static files (like images or CSS files)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Just return the page with no image and report (initial state)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/")
async def predict(file: UploadFile = File(...), 
                  name: str = Form(...), 
                  age: int = Form(...), 
                  gender: str = Form(...), 
                  date: str = Form(...)):

    # 🛠️ Removed 'await' from here
    image_b64, report = predict_tb(file, name, age, gender, date)

    return templates.TemplateResponse("index.html", {
        "request": {},
        "image": image_b64,
        "report": report
    })

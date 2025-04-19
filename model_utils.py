from ultralytics import YOLO
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import cv2

model = YOLO("best (2).pt")


def process_image_and_generate_report(file, name, age, gender, date):
    contents = file.file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image_np = np.array(image)
    results = model.predict(image_np)
    annotated_image = results[0].plot()

    _, buffer = cv2.imencode(".jpg", annotated_image)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    report = {
        "patient_info": {
            "name": name, "age": age, "gender": gender, "date": date
        },
        "findings": "Mock TB result — use real YOLO class analysis here.",
        "notes": "⚠️ AI-generated report. Consult a doctor."
    }
    return image_base64, report

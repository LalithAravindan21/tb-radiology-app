import json
import os

DB = "patients.json"

def save_patient(name, age, gender, date, report):
    if os.path.exists(DB):
        with open(DB, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[name] = {
        "age": age,
        "gender": gender,
        "date": date,
        "report": report
    }

    with open(DB, "w") as f:
        json.dump(data, f, indent=4)


def load_patient(name):
    if not os.path.exists(DB):
        return None
    with open(DB, "r") as f:
        data = json.load(f)
        return data.get(name, None)

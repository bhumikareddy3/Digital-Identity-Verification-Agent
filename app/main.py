from fastapi import FastAPI, UploadFile
from app.orchestrator import run_pipeline
import os

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/verify")
async def verify(file: UploadFile):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = run_pipeline(path)
    return result

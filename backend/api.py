from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from face_detection.face_detector import detect_faces
from PIL import Image
import os
import cv2
import numpy as np
import io

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the age detection API!"}


@app.get("/models")
async def get_models():
    directory_path = "models"

    try:
        files = os.listdir(directory_path)
        if not files:
            raise HTTPException(status_code=404, detail="No models found")
        return JSONResponse(content={"files": files}, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/detect-age/single")
async def detect_age_single(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an image.")
    try:
        content = await file.read()
        image_array = cv2.imdecode(np.frombuffer(content, np.uint8), -1)

        detected_faces = detect_faces(image_array)
        if not detected_faces['faces'].any():
            raise HTTPException(status_code=400, detail="No faces detected in the image.")

        image_pil = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))

        output_image = io.BytesIO()
        image_pil.save(output_image, format="JPEG")

        output_image.seek(0)
        return StreamingResponse(io.BytesIO(output_image.read()), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse(content={"detail": f"An error occurred: {str(e)}"}, status_code=500)

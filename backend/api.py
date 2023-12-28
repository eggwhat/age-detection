from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from core.face_detection import detect_faces
from core.video_processing import generate_video, process_video
from PIL import Image
from typing import List
import shutil
import tempfile
import zipfile
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


@app.post("/detect-age/multiple")
def detect_age_multiple(files: List[UploadFile] = File(...)):
    if not all(file.content_type.startswith("image/") for file in files):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an image.")
    try:
        images = []
        for file in files:
            content = file.file.read()
            image_array = cv2.imdecode(np.frombuffer(content, np.uint8), -1)

            detected_faces = detect_faces(image_array)
            if not detected_faces['faces'].any():
                raise HTTPException(status_code=400, detail="No faces detected in the image.")

            image_pil = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
            output_image = io.BytesIO()
            image_pil.save(output_image, format="PNG")
            output_image.seek(0)
            images.append({"name": file.filename, "content": output_image.getvalue()})

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for image in images:
                zipf.writestr(image["name"], image["content"])

        zip_file.seek(0)
        return StreamingResponse(iter([zip_file.getvalue()]), media_type="application/x-zip-compressed",
                                 headers={"Content-Disposition": f"attachment; filename=images.zip"})
    except Exception as e:
        return JSONResponse(content={"detail": f"An error occurred: {str(e)}"}, status_code=500)


@app.post("/detect-age/video")
async def detect_age_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a video.")
    try:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)

        with open(file_path, "wb") as video_file:
            shutil.copyfileobj(file.file, video_file)

        frames, frame_rate = process_video(file_path, detect_faces)

        video_bytes = generate_video(frames, temp_dir, frame_rate)
        shutil.rmtree(temp_dir)

        return StreamingResponse(io.BytesIO(video_bytes), media_type="video/mp4")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

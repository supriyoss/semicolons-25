"""
Steps:
1. Input Documents(Shared Storage to be decided)
2. Check whether the document is pdf or image
3a. If image proceed to 4.
3b. If pdf, convert to image
4. Mark regions of image for information extraction
5. Apply OCR to the image
6. Send formatted data to the DB(DB yet to be decided)

"""
import os
import uuid
import uvicorn
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="SEMICOLONS-25")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the 'uploads' folder.
    """
    try:
        # Create a unique file name to avoid collisions
        file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{file.filename}")

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {"message": "File uploaded successfully", "file_path": file_path}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) #, reload=True


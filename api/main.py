from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

from fastapi import UploadFile, File
from pyzbar.pyzbar import decode
from PIL import Image
from typing import List
# CORS from fastapi
from fastapi.middleware.cors import CORSMiddleware
import os

# Initialize FastAPI app
app = FastAPI()

# MongoDB configuration
# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Barcode_db"]  # Database name
barcodes_collection = db["food_info"]  # Collection name

# Allow origins for CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class BarcodeRequest(BaseModel):
    code: str

@app.post("/get-nutrition/")
async def get_nutrition(data: BarcodeRequest):
    """
    Fetch nutritional information for the given barcode.

    Args:
        data (BarcodeRequest): Barcode number as a JSON object.

    Returns:
        JSON response with nutritional data or an error message.
    """
    barcode = data.code
    # Query the database for the given barcode
    result = barcodes_collection.find_one({"code": barcode})
    
    if not result:
        raise HTTPException(status_code=404, detail="Barcode not found")
    
    # Remove MongoDB's internal ID field (_id) for cleaner output
    result.pop("_id", None)
    return result

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "API is running. Use the /get-nutrition endpoint.Use the /read-barcode endpoint to decode barcodes."}

@app.post("/read-barcode/")
async def read_barcode(file: UploadFile = File(...)):
    """
    Reads barcode information from an uploaded image.

    Args:
        file (UploadFile): The image file containing the barcode.

    Returns:
        JSON response with barcode data.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        # Read image from uploaded file
        image = Image.open(file.file)
        
        # Decode barcodes in the image
        barcodes = decode(image)
        if not barcodes:
            return {"message": "No barcodes detected in the image."}

        # Extract barcode data
        barcode_data = [{"type": barcode.type, "data": barcode.data.decode("utf-8")} for barcode in barcodes]
        return {"barcodes": barcode_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {e}")


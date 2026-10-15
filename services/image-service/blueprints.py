from fastapi import APIRouter, File, UploadFile, HTTPException
from io_models import AnalysisResponse
from engine.pipeline import analyze_image_bytes

router = APIRouter()
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB

@router.post("/api/v1/analyze-image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()
    
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 15MB limit.")

    try:
        # Pass the raw file bytes into your core engine
        result = analyze_image_bytes(contents)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
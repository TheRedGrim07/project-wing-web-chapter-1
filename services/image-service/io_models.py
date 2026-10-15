from pydantic import BaseModel
from typing import Optional

class ImageMetadata(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    lens: Optional[str] = None
    focal_length: Optional[str] = None
    aperture: Optional[str] = None
    exposure_time: Optional[str] = None
    iso: Optional[int] = None

class AnalysisResponse(BaseModel):
    metadata: ImageMetadata
    is_safe: bool
    moderation_notes: str
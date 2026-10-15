import io
from PIL import Image, UnidentifiedImageError

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}

def validate_and_get_dimensions(contents: bytes) -> tuple[int, int]:
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()  
        
        image = Image.open(io.BytesIO(contents))
        fmt = image.format.upper() if image.format else ""
        if fmt not in ALLOWED_FORMATS:
            raise ValueError(f"Unsupported format: {fmt}. Allowed: JPEG, PNG, WEBP.")
        
        return image.size
    except UnidentifiedImageError:
        raise ValueError("Invalid image file or corrupted data.")
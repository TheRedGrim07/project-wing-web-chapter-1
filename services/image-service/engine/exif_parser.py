import io
import exifread

def format_fraction(val) -> str:
    if hasattr(val, 'num') and hasattr(val, 'den'):
        if val.den == 0: return "0"
        if val.den == 1: return str(val.num)
        return f"{val.num}/{val.den}"
    return str(val)

def calculate_f_number(val) -> str:
    if hasattr(val, 'num') and hasattr(val, 'den') and val.den != 0:
        return f"f/{(val.num / val.den):.1f}"
    return f"f/{val}"

def extract_exif_data(contents: bytes) -> tuple[dict, dict]:
    tags = exifread.process_file(io.BytesIO(contents), details=False)
    
    make = str(tags.get("Image Make")) if "Image Make" in tags else None
    model = str(tags.get("Image Model")) if "Image Model" in tags else None
    
    lens = str(tags.get("EXIF LensModel")) if "EXIF LensModel" in tags else None
    if not lens and "EXIF LensSpecification" in tags:
        lens = str(tags.get("EXIF LensSpecification"))
            
    focal_length = tags.get("EXIF FocalLength")
    focal_length_str = f"{format_fraction(focal_length.values[0])}mm" if focal_length else None

    aperture = tags.get("EXIF FNumber")
    aperture_str = calculate_f_number(aperture.values[0]) if aperture else None

    exposure = tags.get("EXIF ExposureTime")
    exposure_str = f"{format_fraction(exposure.values[0])}s" if exposure else None

    iso_val = tags.get("EXIF ISOSpeedRatings")
    iso = int(iso_val.values[0]) if iso_val else None

    parsed_data = {
        "make": make, "model": model, "lens": lens,
        "focal_length": focal_length_str, "aperture": aperture_str,
        "exposure_time": exposure_str, "iso": iso
    }
    
    return parsed_data, tags
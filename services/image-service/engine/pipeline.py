from io_models import ImageMetadata, AnalysisResponse
from .image_processor import validate_and_get_dimensions
from .exif_parser import extract_exif_data
from .safety_checker import run_heuristics

def analyze_image_bytes(contents: bytes) -> AnalysisResponse:
    width, height = validate_and_get_dimensions(contents)
    parsed_exif, raw_tags = extract_exif_data(contents)
    is_safe, moderation_notes = run_heuristics(width, height, raw_tags)

    metadata = ImageMetadata(
        width=width,
        height=height,
        **parsed_exif
    )

    return AnalysisResponse(
        metadata=metadata,
        is_safe=is_safe,
        moderation_notes="; ".join(moderation_notes) if moderation_notes else "Clean"
    )
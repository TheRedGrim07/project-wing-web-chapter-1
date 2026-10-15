PROHIBITED_KEYWORDS = ["nsfw", "violence", "blood", "gore"]

def run_heuristics(width: int, height: int, raw_tags: dict) -> tuple[bool, list]:
    is_safe = True
    moderation_notes = []

    if width == 0 or height == 0:
        is_safe = False
        moderation_notes.append("Invalid resolution (0 pixels).")
    else:
        aspect_ratio = width / height
        if aspect_ratio > 5.0 or aspect_ratio < 0.2:
            is_safe = False
            moderation_notes.append("Extreme aspect ratio flagged as potential spam.")

    for tag_key, tag_value in raw_tags.items():
        if isinstance(tag_value.values, str):
            if any(keyword in tag_value.values.lower() for keyword in PROHIBITED_KEYWORDS):
                is_safe = False
                moderation_notes.append(f"Prohibited keyword found in metadata tag: {tag_key}.")

    return is_safe, moderation_notes
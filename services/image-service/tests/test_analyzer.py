import pytest
from fastapi.testclient import TestClient
from main import app
import io
from PIL import Image

client = TestClient(app)

def create_dummy_image(format="JPEG", size=(100, 100)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color="blue")
    image.save(file, format=format)
    file.seek(0)
    return file.read()

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "version": "1.0.0"}

def test_image_without_exif():
    """Test standard image without EXIF to ensure strict null-safety."""
    img_bytes = create_dummy_image()
    response = client.post(
        "/api/v1/analyze-image",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["is_safe"] is True
    assert data["metadata"]["width"] == 100
    assert data["metadata"]["height"] == 100
    assert data["metadata"]["make"] is None

def test_invalid_non_image_file():
    """Test rejecting non-image payloads for safety."""
    response = client.post(
        "/api/v1/analyze-image",
        files={"file": ("test.txt", b"Hello World", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid image" in response.json()["detail"] or "Unsupported" in response.json()["detail"]

def test_extreme_aspect_ratio_safety():
    """Test safety heuristics flag extreme aspect ratios."""
    img_bytes = create_dummy_image(size=(1000, 10))
    response = client.post(
        "/api/v1/analyze-image",
        files={"file": ("spam.jpg", img_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json()["is_safe"] is False
    assert "Extreme aspect ratio" in response.json()["moderation_notes"]
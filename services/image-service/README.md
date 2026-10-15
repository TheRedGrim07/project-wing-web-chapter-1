# Image Intelligence Microservice (Python FastAPI)

**Lead Engineer**: `@TheRedGrim07` (Ayush Sinha) & `@sarojsenn` (Saroj Sen)

This service processes uploaded photographs to extract camera EXIF specifications (Make, Model, Lens, Aperture, ISO, Shutter Speed) and performs content validation.

## Local Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   # source venv/bin/activate # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Interactive Swagger documentation:
   Open [http://localhost:8000/docs](http://localhost:8000/docs)

5. Run Test:
   ```bash
   pytest tests/
   ```

6. Structure: 
   services/image-service/
   ├── main.py                 # Application entry point; initializes FastAPI and registers routes
   ├── io_models.py            # Pydantic schemas defining exactly what goes in and out (Input/Output)
   ├── blueprints.py           # FastAPI router defining the HTTP endpoints (e.g., /api/v1   analyze-image)
   ├── requirements.txt        # Python package dependencies (FastAPI, Pillow, exifread, etc.)
   ├── README.md               # Documentation on how to run and test the microservice locally
   ├── engine/                 # Core business logic separated by feature
   │   ├── __init__.py         # Empty file indicating this directory is a Python module
   │   ├── image_processor.py  # Handles Pillow format validation and dimension extraction
   │   ├── exif_parser.py      # Handles exifread parsing and math conversions (fractions, f-stop)
   │   ├── safety_checker.py   # Handles resolution checks, aspect ratio limits, and keyword flagging
   │   └── pipeline.py         # Orchestrates the engine files and returns the final AnalysisResponse
   └── tests/                  # Automated pytest suite
      ├── __init__.py         # Empty file indicating this directory is a test module
      └── test_analyzer.py    # Unit tests for null-safety, non-image files, and aspect ratios



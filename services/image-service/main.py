from fastapi import FastAPI
from blueprints import router as image_router

app = FastAPI(title="Image Analysis Service", version="1.0.0")

@app.get("/")
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "online", "version": "1.0.0"}

# Register the routes defined in blueprints.py
app.include_router(image_router)
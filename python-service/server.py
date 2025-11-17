"""
Minimal FastAPI stub for embeddings service.
Returns mock embeddings for testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Enable CORS for Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmbedRequest(BaseModel):
    folder_path: str


@app.get("/")
def root():
    return {"message": "Cerebro Python service is running"}


@app.post("/embed")
def embed(request: EmbedRequest):
    """
    Mock embedding endpoint.
    Returns a list of 384 random floats as a mock embedding.
    """
    # Generate mock embedding (384 dimensions, common embedding size)
    mock_embedding = [random.uniform(-1, 1) for _ in range(384)]
    
    return {
        "embedding": mock_embedding,
        "folder_path": request.folder_path,
        "dimensions": len(mock_embedding),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


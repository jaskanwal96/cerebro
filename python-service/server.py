"""
Minimal FastAPI stub for embeddings service.
Returns mock embeddings for testing.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sys
import os
import random

# Add services directory to path
services_path = os.path.join(os.path.dirname(__file__), 'services')
sys.path.insert(0, services_path)

import file_reader
from chunker import chunk_text
from embedder import generate_embedding

# Import ChromaDB client
sys.path.insert(0, os.path.dirname(__file__))
from data.chroma_db.client import store_embeddings

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

@app.post("/ingest")
def ingest(request: EmbedRequest):
    """
    Process all files in folder: read → chunk → embed → store_embeddings
    
    Args:
        request: EmbedRequest with folder_path
        
    Returns:
        Summary of ingestion process
    """
    folder_path = request.folder_path
    
    # Validate folder exists
    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=400, detail=f"Folder not found: {folder_path}")
    
    try:
        # Step 1: Read all files in folder
        files = file_reader.read_files_in_folder(folder_path)
        
        if not files:
            return {
                "status": "success",
                "message": "No files found to process",
                "files_processed": 0,
                "total_chunks": 0
            }
        
        # Process each file
        all_chunks = []
        files_processed = []
        
        for filename, content in files.items():
            file_path = os.path.join(folder_path, filename)
            
            # Step 2: Chunk the file
            chunks = chunk_text(
                source_file=filename,
                file_data=content,
                file_path=file_path
            )
            
            all_chunks.extend(chunks)
            files_processed.append({
                "filename": filename,
                "chunks": len(chunks)
            })
        
        if not all_chunks:
            return {
                "status": "success",
                "message": "No chunks created",
                "files_processed": len(files_processed),
                "total_chunks": 0
            }
        
        # Step 3: Generate embeddings for all chunks
        embeddings = generate_embedding(all_chunks)
        
        # Step 4: Store embeddings in ChromaDB
        store_embeddings(all_chunks, embeddings)
        
        return {
            "status": "success",
            "message": f"Successfully ingested {len(files_processed)} file(s)",
            "files_processed": len(files_processed),
            "total_chunks": len(all_chunks),
            "files": files_processed
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


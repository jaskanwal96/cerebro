import chromadb
from pathlib import Path

# Get the path to store ChromaDB data
# __file__ is at: python-service/data/chroma_db/client.py
# So parent = python-service/data/chroma_db/
CHROMA_DB_PATH = Path(__file__).parent

# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

# Get or create collection
collection = chroma_client.get_or_create_collection(name="rag_collection")


def store_embeddings(chunks, embeddings):
    """
    Store chunks and their embeddings in ChromaDB
    
    Args:
        chunks: List of chunk dicts with text, source_file, chunk_index, file_path
        embeddings: numpy array of embeddings
    """
    documents = [chunk["text"] for chunk in chunks]
    ids = [f"{chunk['source_file']}_chunk_{chunk['chunk_index']}" for chunk in chunks]
    metadatas = [
        {
            "source_file": chunk["source_file"],
            "chunk_index": chunk["chunk_index"],
            "file_path": chunk["file_path"]
        }
        for chunk in chunks
    ]
    
    # Convert numpy array to list if needed
    if hasattr(embeddings, 'tolist'):
        embeddings_list = embeddings.tolist()
    else:
        embeddings_list = embeddings
    
    collection.add(
        documents=documents,
        embeddings=embeddings_list,
        ids=ids,
        metadatas=metadatas
    )
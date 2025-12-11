from sentence_transformers import SentenceTransformer
from pathlib import Path
from chunker import chunk_text
import file_reader
import numpy as np

# Better path handling - works from any directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_PATH = PROJECT_ROOT / "assets"

def cosine_similarity_manual(vec1, vec2):
    """
    Calculate cosine similarity between two vectors
    
    Args:
        vec1: numpy array (1D or 2D)
        vec2: numpy array (1D or 2D)
    
    Returns:
        cosine similarity score (0 to 1)
    """
    # Convert to numpy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # Ensure they're 1D
    if vec1.ndim > 1:
        vec1 = vec1.flatten()
    if vec2.ndim > 1:
        vec2 = vec2.flatten()
    
    # Step 1: Calculate dot product
    dot_product = np.dot(vec1, vec2)
    
    # Step 2: Calculate magnitudes (L2 norm)
    magnitude1 = np.linalg.norm(vec1)  # √(ΣAᵢ²)
    magnitude2 = np.linalg.norm(vec2)  # √(ΣBᵢ²)
    
    # Step 3: Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Step 4: Calculate cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)
    
    return similarity

def generate_embedding(chunks):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(chunk_texts)
    return embeddings

def compare_embeddings(text1, text2):
    """Generate embeddings for two texts and calculate their similarity"""
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Generate embeddings
    embedding1 = model.encode([text1])
    embedding2 = model.encode([text2])
    
    # Calculate cosine similarity
    similarity = cosine_similarity_manual(embedding1, embedding2)
    
    print(f"Text 1: '{text1}'")
    print(f"Text 2: '{text2}'")
    print(f"Cosine Similarity: {similarity:.4f}")
    print(f"Similarity %: {similarity * 100:.2f}%")
    print("-" * 50)
    
    return similarity
# Test code - only runs when script is executed directly
if __name__ == "__main__":
    files = file_reader.read_files_in_folder(str(ASSETS_PATH))
    chunks = chunk_text('test', files['test.txt'])
    generate_embedding(chunks)
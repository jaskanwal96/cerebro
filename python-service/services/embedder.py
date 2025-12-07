from sentence_transformers import SentenceTransformer
from pathlib import Path
from chunker import chunk_text
import file_reader

# Better path handling - works from any directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_PATH = PROJECT_ROOT / "assets"


def generate_embedding(chunks):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    print(embeddings)
    return embeddings


# Test code - only runs when script is executed directly
if __name__ == "__main__":
    files = file_reader.read_files_in_folder(str(ASSETS_PATH))
    print(files)
    chunks = chunk_text('testing_learning_guide', files['testing_learning_guide.md'])
    print(chunks)
    generate_embedding(chunks)
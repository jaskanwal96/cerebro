# Cerebro Learning Guide: Building RAG + MCP + LLMs

This guide will walk you through building Cerebro step-by-step, explaining concepts as you implement them.

## Prerequisites Check

Before starting, make sure you understand:
- ✅ Basic JavaScript/TypeScript
- ✅ Async/await and Promises
- ✅ REST APIs (HTTP requests)
- ✅ Basic file system operations

If you're unsure about any of these, review them first!

---

## Phase 2: Implementation Steps

### Step 1: Document Ingestion Pipeline

**Goal**: Take files from a folder → chunk them → generate embeddings → store in a vector database

**Why this matters**: This is the foundation of RAG. Without ingesting and storing documents, you can't retrieve them later.

#### Step 1.1: Set Up Your Python Service Structure

**What you'll learn**: Organizing a FastAPI service for document processing

**Tasks**:
1. Create a `python-service/services/` folder
2. Create `python-service/services/file_reader.py` - handles reading different file types
3. Create `python-service/services/chunker.py` - splits documents into chunks
4. Create `python-service/services/embedder.py` - generates embeddings

**Key Concepts**:
- **File Reading**: Different file types (`.txt`, `.md`, `.pdf`) need different parsers
- **Chunking**: Documents are too large for LLMs, so we split them into smaller pieces
- **Embeddings**: Convert text chunks into numerical vectors that capture meaning

**Questions to answer**:
- What file types should you support initially? (Start with `.txt` and `.md`)
- How big should chunks be? (Typically 500-1000 characters with overlap)
- What embedding model to use? (Start with `sentence-transformers/all-MiniLM-L6-v2` - it's free and local)

**Implementation hints**:
```python
# file_reader.py structure
def read_text_file(file_path: str) -> str:
    # Read .txt files
    pass

def read_markdown_file(file_path: str) -> str:
    # Read .md files
    pass

# chunker.py structure
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    # Split text into overlapping chunks
    # Why overlap? To preserve context at boundaries
    pass

# embedder.py structure
def generate_embedding(text: str) -> List[float]:
    # Use sentence-transformers to create embeddings
    # Returns a list of floats (vector)
    pass
```

**Resources**:
- [sentence-transformers docs](https://www.sbert.net/)
- [Text chunking strategies](https://www.pinecone.io/learn/chunking-strategies/)

---

#### Step 1.2: Implement File Reader

**What you'll learn**: Handling different file types and error cases

**Tasks**:
1. Implement basic text file reading
2. Add markdown support
3. Handle encoding issues (UTF-8)
4. Add error handling for unreadable files

**Key Concepts**:
- **Encoding**: Files can be in different encodings, UTF-8 is most common
- **Error Handling**: Some files might be corrupted or binary - handle gracefully

**Implementation checklist**:
- [ ] Read `.txt` files
- [ ] Read `.md` files  
- [ ] Handle file not found errors
- [ ] Handle encoding errors
- [ ] Return clean text (strip extra whitespace)

**Test it**:
Create a test folder with a few `.txt` and `.md` files, then verify your reader can extract text from them.

---

#### Step 1.3: Implement Chunker

**What you'll learn**: Why and how to split documents intelligently

**Tasks**:
1. Implement simple character-based chunking
2. Add overlap between chunks
3. Try to split at sentence boundaries (better than mid-sentence)

**Key Concepts**:
- **Chunk Size**: Too small = lose context, too large = exceed LLM limits
- **Overlap**: Prevents losing context at chunk boundaries
- **Boundary Detection**: Split at sentences/paragraphs when possible

**Why overlap matters**:
```
Document: "The cat sat on the mat. The dog barked loudly."
Chunk 1: "The cat sat on the mat. The dog"
Chunk 2: "The dog barked loudly."
```
Without overlap, "The dog" context is lost between chunks.

**Implementation checklist**:
- [ ] Split text into chunks of specified size
- [ ] Add overlap between chunks
- [ ] Try to split at sentence boundaries (use `. ` or `\n\n`)
- [ ] Handle edge cases (very short documents, very long sentences)

**Test it**:
Take a long text document and verify chunks are created with proper overlap.

---

#### Step 1.4: Implement Embedder

**What you'll learn**: Converting text to numerical vectors

**Tasks**:
1. Install `sentence-transformers`: `pip install sentence-transformers`
2. Load a model (start with `all-MiniLM-L6-v2` - small and fast)
3. Generate embeddings for text chunks
4. Understand what embeddings represent

**Key Concepts**:
- **Embeddings**: Dense vectors that capture semantic meaning
- **Similarity**: Similar texts have similar embeddings (measured by cosine similarity)
- **Model Choice**: Trade-off between quality, speed, and size

**What embeddings look like**:
```python
text = "The cat sat on the mat"
embedding = [0.123, -0.456, 0.789, ...]  # 384 numbers for MiniLM
```

**Implementation checklist**:
- [ ] Load sentence-transformers model
- [ ] Generate embedding for a single text
- [ ] Batch process multiple texts (faster)
- [ ] Return embeddings as lists of floats

**Test it**:
Generate embeddings for "cat" and "kitten" - they should be more similar than "cat" and "airplane".

**Resources**:
- [Sentence Transformers Quick Start](https://www.sbert.net/docs/quickstart.html)
- [Understanding Embeddings](https://platform.openai.com/docs/guides/embeddings)

---

#### Step 1.5: Set Up Vector Database

**What you'll learn**: Storing and querying embeddings efficiently

**Tasks**:
1. Choose a vector database (start with SQLite + `sqlite-vss` or `chromadb` for simplicity)
2. Create schema to store: chunk text, embedding, metadata (file path, chunk index)
3. Implement insert function
4. Implement similarity search function

**Key Concepts**:
- **Vector Database**: Optimized for storing and searching high-dimensional vectors
- **Metadata**: Store original text + file info alongside embeddings
- **Similarity Search**: Find vectors closest to a query vector

**Option 1: ChromaDB (Easiest)**
```python
# Simple, Python-native, good for learning
pip install chromadb
```

**Option 2: SQLite + sqlite-vss (More control)**
```python
# Uses SQLite you already know, but requires extension
```

**Recommendation**: Start with **ChromaDB** - it's designed for learning and prototyping.

**Implementation checklist**:
- [ ] Install vector database library
- [ ] Create collection/database
- [ ] Store chunks with embeddings and metadata
- [ ] Implement similarity search (query embedding → top K results)

**Key metadata to store**:
- Original chunk text
- Source file path
- Chunk index (position in document)
- Timestamp

**Test it**:
1. Store a few chunks with embeddings
2. Search for similar chunks to a query
3. Verify you get relevant results back

**Resources**:
- [ChromaDB Quick Start](https://docs.trychroma.com/getting-started)
- [Vector Database Concepts](https://www.pinecone.io/learn/vector-database/)

---

#### Step 1.6: Create Ingestion Endpoint

**What you'll learn**: Connecting file processing to your API

**Tasks**:
1. Create `/ingest` endpoint in FastAPI
2. Accept folder path from Electron
3. Process all files in folder: read → chunk → embed → store
4. Return progress/status

**Key Concepts**:
- **Async Processing**: File processing can be slow - use async/await
- **Progress Tracking**: Users want to know what's happening
- **Error Handling**: Some files might fail - continue with others

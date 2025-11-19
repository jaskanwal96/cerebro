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

**Implementation checklist**:
- [ ] Create POST `/ingest` endpoint
- [ ] Accept `folder_path` in request body
- [ ] Walk through folder, find supported files
- [ ] Process each file: read → chunk → embed → store
- [ ] Return summary: files processed, chunks created, errors
- [ ] Handle errors gracefully (log and continue)

**Response format**:
```json
{
  "success": true,
  "files_processed": 5,
  "chunks_created": 47,
  "errors": []
}
```

**Test it**:
Call the endpoint from Electron with a test folder and verify files are processed.

---

### Step 2: Query and Retrieval

**Goal**: User query → embed query → find similar chunks → return top K results

**Why this matters**: This is the "Retrieval" part of RAG. You need to find the most relevant chunks for a user's question.

#### Step 2.1: Implement Query Embedding

**What you'll learn**: Treating user queries the same as documents

**Tasks**:
1. Create `/query` endpoint
2. Accept user query text
3. Generate embedding for query (same model as documents)
4. Return query embedding

**Key Concepts**:
- **Query Embedding**: User questions get embedded the same way as documents
- **Semantic Search**: Find documents that mean similar things, not just exact matches

**Why this works**:
- Query: "What did the cat do?"
- Document chunk: "The cat sat on the mat"
- These have similar embeddings even though words don't match!

**Implementation checklist**:
- [ ] Create POST `/query` endpoint
- [ ] Accept `query_text` in request body
- [ ] Generate embedding using same embedder
- [ ] Return embedding (for now, just to test)

**Test it**:
Send a query and verify you get an embedding back.

---

#### Step 2.2: Implement Similarity Search

**What you'll learn**: Finding the most relevant chunks

**Tasks**:
1. Use vector database to search for similar embeddings
2. Return top K results (start with K=5)
3. Include metadata (source file, chunk text, similarity score)

**Key Concepts**:
- **Cosine Similarity**: Measures angle between vectors (0 = identical, 1 = opposite)
- **Top-K Retrieval**: Return the K most similar chunks
- **Relevance Score**: How similar the chunk is to the query

**Implementation checklist**:
- [ ] Implement similarity search in vector DB
- [ ] Return top K chunks (K=5 to start)
- [ ] Include similarity scores
- [ ] Include full metadata (text, file path, chunk index)

**Response format**:
```json
{
  "results": [
    {
      "text": "The cat sat on the mat...",
      "file_path": "/path/to/file.txt",
      "chunk_index": 2,
      "similarity": 0.87
    },
    ...
  ]
}
```

**Test it**:
1. Ingest some documents about cats
2. Query "What did the cat do?"
3. Verify you get relevant chunks back, not random ones

**Resources**:
- [Cosine Similarity Explained](https://www.machinelearningplus.com/nlp/cosine-similarity/)

---

#### Step 2.3: Add Query Refinement

**What you'll learn**: Improving retrieval quality

**Tasks**:
1. Experiment with different K values (3, 5, 10)
2. Add minimum similarity threshold (filter out irrelevant results)
3. Try query expansion (add related terms)

**Key Concepts**:
- **K Value**: More results = more context but potentially less relevant
- **Threshold**: Filter out results below a similarity score
- **Query Expansion**: Add synonyms/related terms to improve matching

**Implementation checklist**:
- [ ] Make K configurable
- [ ] Add similarity threshold parameter
- [ ] Filter results below threshold
- [ ] (Optional) Try simple query expansion

**Test it**:
Try different K values and thresholds to see how results change.

---

### Step 3: LLM Integration

**Goal**: Retrieved chunks + user query → LLM → coherent answer

**Why this matters**: This is the "Generation" part of RAG. The LLM synthesizes retrieved context into an answer.

#### Step 3.1: Set Up Local LLM (Ollama)

**What you'll learn**: Running LLMs locally vs using APIs

**Tasks**:
1. Install Ollama: https://ollama.ai
2. Pull a small model: `ollama pull llama3.2:1b` (or `mistral:7b` for better quality)
3. Test it from command line
4. Understand model sizes and trade-offs

**Key Concepts**:
- **Local vs API**: Local = private, free, slower. API = faster, costs money, data leaves your machine
- **Model Size**: Bigger = smarter but slower. Start small for learning.
- **Context Window**: Maximum tokens the model can process at once

**Why Ollama?**
- Free and local (privacy)
- Easy to use
- Good for learning
- Can switch to API later

**Test it**:
```bash
ollama run llama3.2:1b "What is a cat?"
```

**Resources**:
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Model Comparison](https://ollama.com/library)

---

#### Step 3.2: Create LLM Service

**What you'll learn**: Calling LLMs programmatically

**Tasks**:
1. Create `python-service/services/llm_service.py`
2. Implement function to call Ollama API
3. Handle responses and errors
4. Understand prompt construction

**Key Concepts**:
- **Prompt Engineering**: How you ask questions matters
- **Context Management**: LLMs have token limits - manage context carefully
- **Streaming**: LLMs can stream responses (show as they generate)

**Implementation checklist**:
- [ ] Install `requests` or use `ollama` Python library
- [ ] Create function to call Ollama
- [ ] Handle API errors
- [ ] Return generated text

**Basic structure**:
```python
def call_llm(prompt: str, model: str = "llama3.2:1b") -> str:
    # Call Ollama API
    # Return response
    pass
```

**Test it**:
Call your LLM service with a simple prompt and verify you get a response.

**Resources**:
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Ollama API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)

---

#### Step 3.3: Construct RAG Prompt

**What you'll learn**: How to combine retrieved context with user query

**Tasks**:
1. Create prompt template that includes:
   - Retrieved chunks (context)
   - User query
   - Instructions for the LLM
2. Handle token limits (truncate if needed)
3. Format prompt clearly

**Key Concepts**:
- **Prompt Template**: Structured way to combine context + query
- **Token Limits**: Models have max context - count tokens and truncate
- **Clear Instructions**: Tell LLM how to use the context

**Prompt structure**:
```
You are a helpful assistant. Use the following context to answer the question.

Context:
[Retrieved chunk 1]
[Retrieved chunk 2]
...

Question: {user_query}

Answer:
```

**Implementation checklist**:
- [ ] Create prompt template function
- [ ] Insert retrieved chunks into context section
- [ ] Add user query
- [ ] Add clear instructions
- [ ] Handle token limits (estimate and truncate if needed)

**Test it**:
Construct a prompt with some test chunks and query, verify format looks good.

**Resources**:
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [RAG Prompt Patterns](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

#### Step 3.4: Create RAG Endpoint

**What you'll learn**: Putting it all together

**Tasks**:
1. Create `/rag` endpoint that:
   - Takes user query
   - Retrieves relevant chunks (Step 2)
   - Constructs prompt (Step 3.3)
   - Calls LLM (Step 3.2)
   - Returns answer
2. Handle errors at each step
3. Return structured response

**Key Concepts**:
- **End-to-End Flow**: Query → Retrieve → Generate → Return
- **Error Handling**: Each step can fail - handle gracefully
- **Response Format**: Return both answer and sources (for transparency)

**Implementation checklist**:
- [ ] Create POST `/rag` endpoint
- [ ] Accept `query` in request body
- [ ] Call retrieval (Step 2.2)
- [ ] Construct prompt with retrieved chunks
- [ ] Call LLM with prompt
- [ ] Return answer + source chunks
- [ ] Handle errors at each step

**Response format**:
```json
{
  "answer": "The cat sat on the mat...",
  "sources": [
    {
      "text": "...",
      "file_path": "...",
      "similarity": 0.87
    }
  ]
}
```

**Test it**:
1. Ingest some documents
2. Send a query to `/rag`
3. Verify you get a coherent answer based on your documents

---

### Step 4: MCP Integration

**Goal**: Expose your RAG system as MCP tools that other applications can use

**Why this matters**: MCP lets you build composable AI tools. Your RAG system becomes a tool others can use.

#### Step 4.1: Understand MCP Protocol

**What you'll learn**: How MCP works conceptually

**Tasks**:
1. Read MCP documentation
2. Understand MCP server vs client
3. Understand tools, resources, and prompts concepts
4. See example MCP servers

**Key Concepts**:
- **MCP Server**: Exposes capabilities (tools) via standard protocol
- **MCP Client**: Uses tools from servers
- **Tools**: Functions that can be called (like your RAG endpoint)
- **Protocol**: Standard way to communicate (JSON-RPC over stdio/HTTP)

**MCP Flow**:
```
Client → MCP Server: "Call tool 'search_documents' with query='cats'"
MCP Server → Your RAG: Process query
Your RAG → MCP Server: Return answer
MCP Server → Client: Return result
```

**Resources**:
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)

---

#### Step 4.2: Install MCP SDK

**What you'll learn**: Using the MCP Python SDK

**Tasks**:
1. Install MCP Python SDK: `pip install mcp`
2. Understand basic server structure
3. Create a minimal MCP server example

**Key Concepts**:
- **SDK**: Provides helpers for MCP protocol
- **Server Setup**: Initialize server, register tools, handle requests
- **Tool Definition**: Describe what your tool does, parameters, etc.

**Basic structure**:
```python
from mcp.server import Server
from mcp.types import Tool

server = Server("cerebro-rag")

@server.list_tools()
async def list_tools() -> list[Tool]:
    # Return list of available tools
    pass

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> dict:
    # Handle tool calls
    pass
```

**Implementation checklist**:
- [ ] Install MCP SDK
- [ ] Create basic server structure
- [ ] Define a simple test tool
- [ ] Test server can be called

**Resources**:
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

#### Step 4.3: Expose RAG as MCP Tool

**What you'll learn**: Making your RAG system accessible via MCP

**Tasks**:
1. Create MCP tool: `search_documents`
2. Tool should accept `query` parameter
3. Tool should call your RAG endpoint internally
4. Return formatted result

**Key Concepts**:
- **Tool Definition**: Describe parameters, types, descriptions
- **Tool Execution**: Call your existing RAG code
- **Result Format**: MCP expects specific format

**Tool definition**:
```python
Tool(
    name="search_documents",
    description="Search ingested documents using RAG",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query"
            }
        },
        "required": ["query"]
    }
)
```

**Implementation checklist**:
- [ ] Define `search_documents` tool
- [ ] Accept `query` parameter
- [ ] Call your RAG endpoint/function
- [ ] Format response for MCP
- [ ] Handle errors

**Test it**:
Call your MCP server with a tool request and verify it returns RAG results.

---

#### Step 4.4: Add More MCP Tools

**What you'll learn**: Building a toolkit of capabilities

**Tasks**:
1. Add `ingest_folder` tool (calls your ingestion endpoint)
2. Add `list_documents` tool (shows what's been ingested)
3. Add `clear_database` tool (resets vector store)

**Key Concepts**:
- **Tool Composition**: Multiple tools work together
- **Tool Design**: Think about what operations users need
- **Tool Descriptions**: Clear descriptions help LLMs use tools correctly

**Implementation checklist**:
- [ ] Add `ingest_folder` tool
- [ ] Add `list_documents` tool
- [ ] Add `clear_database` tool
- [ ] Test each tool independently
- [ ] Test tools work together

---

#### Step 4.5: Connect MCP Server to Electron

**What you'll learn**: Using MCP from your Electron app

**Tasks**:
1. Install MCP client in Electron (or use HTTP if MCP server supports it)
2. Call MCP tools from Electron UI
3. Display results in UI

**Key Concepts**:
- **MCP Client**: Connects to MCP servers
- **Tool Invocation**: Call tools by name with parameters
- **Response Handling**: Process tool results

**Implementation options**:
- **Option 1**: Run MCP server as subprocess, communicate via stdio
- **Option 2**: Run MCP server as HTTP server, call via HTTP
- **Option 3**: Call your FastAPI endpoints directly (simpler, but not "true" MCP)

**For learning**: Start with Option 3 (direct FastAPI calls), then add MCP layer later.

**Implementation checklist**:
- [ ] Decide on MCP integration approach
- [ ] Implement MCP client calls from Electron
- [ ] Update UI to use MCP tools
- [ ] Test end-to-end flow

---

### Step 5: UI Integration

**Goal**: Connect everything in a user-friendly Electron UI

**Why this matters**: Users need a way to interact with your RAG system.

#### Step 5.1: Update Folder Ingestion UI

**What you'll learn**: Connecting UI actions to backend

**Tasks**:
1. Update "Choose Folder" button to call `/ingest` endpoint
2. Show progress while ingesting
3. Display results (files processed, chunks created)
4. Handle errors gracefully

**Key Concepts**:
- **Async UI Updates**: Long operations need progress indicators
- **Error Display**: Show users what went wrong
- **State Management**: Track ingestion status

**Implementation checklist**:
- [ ] Call `/ingest` endpoint when folder is selected
- [ ] Show loading state during ingestion
- [ ] Display ingestion results
- [ ] Show errors if ingestion fails
- [ ] Disable buttons during processing

---

#### Step 5.2: Add Query Interface

**What you'll learn**: Building a search interface

**Tasks**:
1. Add query input field
2. Add "Search" button
3. Call `/rag` endpoint with query
4. Display answer and sources

**Key Concepts**:
- **User Input**: Text input, validation
- **Loading States**: Show progress during LLM generation
- **Result Display**: Format answer and show sources

**Implementation checklist**:
- [ ] Add query input field
- [ ] Add search button
- [ ] Call `/rag` endpoint
- [ ] Display answer prominently
- [ ] Show source chunks (collapsible)
- [ ] Show similarity scores
- [ ] Handle streaming responses (if implemented)

---

#### Step 5.3: Polish and Error Handling

**What you'll learn**: Making a production-ready UI

**Tasks**:
1. Add proper error messages
2. Add loading indicators
3. Add empty states
4. Improve styling
5. Add keyboard shortcuts

**Key Concepts**:
- **UX Best Practices**: Clear feedback, helpful errors
- **Accessibility**: Keyboard navigation, screen readers
- **Visual Design**: Clean, modern interface

**Implementation checklist**:
- [ ] Add error toasts/notifications
- [ ] Add loading spinners
- [ ] Add empty states (no documents, no results)
- [ ] Improve Tailwind styling
- [ ] Add Enter key to submit query
- [ ] Add keyboard shortcuts

---

## Testing Strategy

As you build each step, test it:

1. **Unit Tests**: Test individual functions (chunker, embedder, etc.)
2. **Integration Tests**: Test endpoints work together
3. **Manual Testing**: Use the UI, try edge cases
4. **Error Testing**: Try invalid inputs, missing files, etc.

## Common Pitfalls to Avoid

1. **Skipping error handling**: Things will fail - handle it
2. **Ignoring token limits**: LLMs have context limits - respect them
3. **Poor chunking**: Bad chunks = bad retrieval = bad answers
4. **Not testing incrementally**: Test each step before moving on
5. **Over-engineering**: Start simple, add complexity later

## Next Steps After Phase 2

Once you have the basics working:

1. **Improve chunking**: Better strategies (semantic, recursive)
2. **Add re-ranking**: Improve retrieval quality
3. **Support more file types**: PDFs, images, etc.
4. **Add metadata filtering**: Filter by file type, date, etc.
5. **Implement streaming**: Show LLM responses as they generate
6. **Add caching**: Cache embeddings and responses
7. **Optimize performance**: Batch processing, async operations

## Getting Help

When stuck:
1. Read error messages carefully
2. Check documentation for libraries you're using
3. Test components in isolation
4. Use print statements / console.log to debug
5. Search for similar issues online

## Remember

- **Learning > Perfection**: It's okay if it's not perfect initially
- **Iterate**: Build, test, improve, repeat
- **Understand why**: Don't just copy code - understand concepts
- **Start simple**: Add complexity gradually
- **Have fun**: This is exciting technology - enjoy learning it!

---

## Quick Reference: Implementation Order

1. ✅ File reader (read .txt, .md files)
2. ✅ Chunker (split into chunks with overlap)
3. ✅ Embedder (generate embeddings)
4. ✅ Vector database (store and search)
5. ✅ Ingestion endpoint (process folders)
6. ✅ Query endpoint (embed queries)
7. ✅ Similarity search (find relevant chunks)
8. ✅ LLM service (call Ollama)
9. ✅ RAG endpoint (retrieve + generate)
10. ✅ MCP server (expose as tools)
11. ✅ UI updates (connect everything)

Start with Step 1.1 and work through sequentially. Each step builds on the previous one.

Good luck! 🚀


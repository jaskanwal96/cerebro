# Cerebro

A desktop application for learning and experimenting with **RAG (Retrieval-Augmented Generation)**, **MCP (Model Context Protocol)**, and **LLMs (Large Language Models)**.

Cerebro is a personal learning project that combines:
- **Electron** + **React** + **Vite** for the desktop UI
- **Python FastAPI** for document processing and RAG pipeline
- **Local LLMs** (via Ollama) for private, on-device AI
- **Vector databases** for semantic search
- **MCP** for exposing RAG capabilities as composable tools

## What I'm Learning

This project is designed to understand:
- How **RAG** works: document ingestion → chunking → embedding → retrieval → generation
- How **MCP** enables composable AI tools and standardized LLM integrations
- How **LLMs** process context and generate responses
- How to build end-to-end AI applications from scratch

See [`LEARNING_GUIDE.md`](./LEARNING_GUIDE.md) for the step-by-step learning plan.

## Installation

### Node.js Dependencies

```bash
npm install
```

### Python Dependencies

```bash
cd python-service
pip install -r requirements.txt
```

## Running the App

You need to run three services in separate terminals:

### Terminal 1: Python Service
```bash
cd python-service
python server.py
```
The Python service will run on `http://localhost:8000`

### Terminal 2: Vite Dev Server
```bash
npm run dev:ui
```
The Vite dev server will run on `http://localhost:5173`

### Terminal 3: Electron App
```bash
npm run dev:electron
```
This will launch the Electron desktop application.

## Current Status

🚧 **In Progress**: Building the RAG pipeline step by step following the learning guide.

**Currently Working On**:
- Document ingestion (file reading, chunking, embedding generation)
- Vector database setup for semantic search
- LLM integration with Ollama
- MCP server implementation

**Planned Features**:
- 📁 **Document Ingestion**: Process folders of documents (text, markdown, PDFs)
- 🔍 **Semantic Search**: Query documents using embeddings and vector similarity
- 🤖 **RAG Pipeline**: Retrieve relevant context → Generate answers with LLMs
- 🔧 **MCP Tools**: Expose RAG capabilities via Model Context Protocol
- 🖥️ **Desktop UI**: Electron app with React for folder selection, queries, and results

## Features (Current Boilerplate)

- **Choose Folder**: Button to select a folder using Electron's native dialog
- **Summarize Now**: Button that calls the Python FastAPI service (currently mock implementation)
- **Secure IPC**: Uses `contextIsolation: true` for secure communication between main and renderer processes

## Project Structure

```
cerebro/
├── electron-main.js           # Electron main process
├── preload.js                 # Preload script (secure IPC bridge)
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── index.html                 # HTML entry point
├── LEARNING_GUIDE.md          # Step-by-step learning guide
├── src/
│   ├── main.jsx               # React entry point
│   ├── App.jsx                # Main React component
│   └── index.css              # Tailwind CSS imports
└── python-service/
    ├── server.py              # FastAPI server
    ├── requirements.txt        # Python dependencies
    └── services/              # RAG pipeline services
        ├── file_reader.py     # Document reading (text, markdown, etc.)
        ├── chunker.py         # Text chunking strategies
        ├── embedder.py        # Embedding generation
        └── llm_service.py     # LLM integration (Ollama)
```

## Learning Resources

- [`LEARNING_GUIDE.md`](./LEARNING_GUIDE.md) - Complete step-by-step guide for building the RAG system
- Follow the guide to implement each component and understand how RAG, MCP, and LLMs work together

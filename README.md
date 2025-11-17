# Cerebro

Minimal boilerplate for a desktop app using Electron, React, Vite, and Python FastAPI.

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

## Features

- **Choose Folder**: Button to select a folder using Electron's native dialog
- **Summarize Now**: Button that calls the Python FastAPI service to get a mock embedding/summary
- **Secure IPC**: Uses `contextIsolation: true` for secure communication between main and renderer processes

## Project Structure

```
cerebro/
├── electron-main.js      # Electron main process
├── preload.js            # Preload script (secure IPC bridge)
├── vite.config.js        # Vite configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── index.html            # HTML entry point
├── src/
│   ├── main.jsx          # React entry point
│   ├── App.jsx           # Main React component
│   └── index.css         # Tailwind CSS imports
└── python-service/
    ├── server.py         # FastAPI stub with /embed endpoint
    └── requirements.txt  # Python dependencies
```

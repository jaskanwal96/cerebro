import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Choose folder dialog
  chooseFolder: () => ipcRenderer.invoke('choose-folder'),

  // Summarize now (calls Python service via main process)
  summarizeNow: (folderPath) => ipcRenderer.invoke('summarize-now', folderPath),
});


import { useState } from 'react';

function App() {
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChooseFolder = async () => {
    const folderPath = await window.electronAPI.chooseFolder();
    if (folderPath) {
      setSelectedFolder(folderPath);
      setSummary(null); // Clear previous summary
    }
  };

  const handleSummarize = async () => {
    if (!selectedFolder) {
      alert('Please choose a folder first');
      return;
    }

    setLoading(true);
    try {
      const result = await window.electronAPI.summarizeNow(selectedFolder);
      if (result.success) {
        setSummary(result.summary);
      } else {
        setSummary(`Error: ${result.error}`);
      }
    } catch (error) {
      setSummary(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">Cerebro</h1>

        <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
          {/* Folder Chooser */}
          <div>
            <button
              onClick={handleChooseFolder}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
            >
              Choose Folder
            </button>
            {selectedFolder && (
              <p className="mt-2 text-sm text-gray-600">
                Selected: <span className="font-mono">{selectedFolder}</span>
              </p>
            )}
          </div>

          {/* Summarize Button */}
          <div>
            <button
              onClick={handleSummarize}
              disabled={!selectedFolder || loading}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {loading ? 'Processing...' : 'Summarize Now'}
            </button>
          </div>

          {/* Summary Display */}
          {summary && (
            <div className="mt-4 p-4 bg-gray-50 rounded border">
              <h2 className="font-semibold mb-2">Summary:</h2>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{summary}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;


import React, { useState, useRef } from "react";
import axios from "axios";

export default function MetricsForm() {
  const [projectDir, setProjectDir] = useState("");
  const [ignoreDirs, setIgnoreDirs] = useState("node_modules,build,.next");
  const [outputDir, setOutputDir] = useState("reports");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const dirInputRef = useRef(null);
    const fileInputRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
            // If user selected files/folder via the picker, send files instead of a path
            if (selectedFiles && selectedFiles.length > 0) {
                // mark this request as an upload and append each file
                formData.append("uploaded", "true");
                selectedFiles.forEach((f) => formData.append("project_files", f));
            } else {
                formData.append("project_dir", projectDir);
            }
      formData.append("ignore_dirs", ignoreDirs);
      formData.append("output_dir", outputDir);

  const apiBase = import.meta.env.VITE_API_BASE;
  const res = await axios.post(`${apiBase}/api/analyze/`, formData);
      setResult(res.data);
    } catch (err) {
  setError("Error analyzing project. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

    const handleDirPick = () => {
        if (dirInputRef.current) dirInputRef.current.click();
    };

    const handleFilePick = () => {
        if (fileInputRef.current) fileInputRef.current.click();
    };

    const onFilesSelected = (e) => {
        const files = Array.from(e.target.files || []);
        setSelectedFiles(files);
        // Clear projectDir string since user chose files directly
        if (files.length > 0) setProjectDir("");
    };

    const clearSelection = () => {
        setSelectedFiles([]);
    };

    const selectedFileNames = selectedFiles.map((f) => f.webkitRelativePath || f.name);
    const selectedFolder = selectedFileNames.length > 0 && selectedFileNames[0].includes("/")
        ? selectedFileNames[0].split("/")[0]
        : null;

const getReportPath = () => {
    if (!projectDir) return outputDir || "";
    // const usesBackslash = projectDir.includes("\\") && !projectDir.includes("/");
    // const sep = usesBackslash ? "\\" : "/";
    // const trimmed = projectDir.replace(/[\\/]+$/g, "");
    return `${outputDir}`;
};

return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-10 w-full max-w-2xl transition-all">
        <h2 className="text-3xl font-bold mb-8 text-blue-600 dark:text-blue-400 text-center">
            Code Metrics Analyzer
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                    Project Directory
                </label>
                <input
                    type="text"
                    value={projectDir}
                    onChange={(e) => setProjectDir(e.target.value)}
                    // required
                    placeholder="Complete path to your project"
                    className="w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-100"
                />
            </div>

            <div className="flex items-center gap-3">
                <button
                    type="button"
                    onClick={handleDirPick}
                    className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-3 rounded"
                >
                    Choose Folder
                </button>

                <div className="text-sm text-gray-600 dark:text-gray-300 flex-1">
                    {selectedFiles.length > 0 ? (
                        <div>
                            {selectedFolder && (
                                <div className="mb-1 font-medium">Selected folder: {selectedFolder}</div>
                            )}
                            <div className="max-h-40 overflow-auto bg-white dark:bg-gray-800 p-2 rounded">
                                <ul className="text-sm list-disc list-inside">
                                    {selectedFileNames.map((n, i) => (
                                        <li key={i} className="truncate">{n}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    ) : (
                        "No files selected"
                    )}
                </div>

                {/* Hidden inputs for folder/file pickers */}
                <input
                    ref={dirInputRef}
                    type="file"
                    webkitdirectory="true"
                    directory="true"
                    multiple
                    onChange={onFilesSelected}
                    style={{ display: "none" }}
                />

                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    onChange={onFilesSelected}
                    style={{ display: "none" }}
                />
                <button
                    type="button"
                    onClick={clearSelection}
                    className="ml-3 bg-red-100 hover:bg-red-200 dark:bg-red-800 dark:hover:bg-red-700 text-red-700 dark:text-red-200 py-2 px-3 rounded"
                >
                    Clear Selection
                </button>
            </div>

            <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                    Ignore Folders
                </label>
                <input
                    type="text"
                    value={ignoreDirs}
                    onChange={(e) => setIgnoreDirs(e.target.value)}
                    className="w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-100"
                />
            </div>

            <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                    Output Directory
                </label>
                <input
                    type="text"
                    value={outputDir}
                    onChange={(e) => setOutputDir(e.target.value)}
                    className="w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-100"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? "Analyzing..." : "Run Analysis"}
            </button>
        </form>

        {error && (
            <p className="mt-6 text-red-600 dark:text-red-400 font-semibold text-center">{error}</p>
        )}

        {result && (
            <div className="mt-8 bg-gray-100 dark:bg-gray-700 p-5 rounded-lg shadow-inner text-left">
                <h3 className="text-lg font-semibold mb-3 text-blue-700 dark:text-blue-300">
                    Analysis Complete
                </h3>

                <p className="font-medium mb-2">Reports saved to:</p>
                <pre className="bg-white dark:bg-gray-600 rounded p-2 text-sm overflow-auto">
                    {getReportPath()}
                </pre>
            </div>
        )}
    </div>
);
}
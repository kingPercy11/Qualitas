import React, { useState } from "react";
import axios from "axios";

export default function MetricsForm() {
  const [projectDir, setProjectDir] = useState("");
  const [ignoreDirs, setIgnoreDirs] = useState("node_modules,build,.next");
  const [outputDir, setOutputDir] = useState("reports");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("project_dir", projectDir);
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
                    required
                    placeholder="Complete path to your project"
                    className="w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-100"
                />
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
                    {/* {getReportPath()} */}
                </pre>
            </div>
        )}
    </div>
);
}
import React from "react";
import MetricsForm from "../components/MetricsForm";

const Metrics = () => {
  return (
    <div className="min-h-screen bg-linear-to-br from-gray-50 via-white to-gray-200 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-all">
      <header className="text-center py-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">
          Metrics Analyzer
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Run code quality and complexity analysis on your project.
        </p>
      </header>

      {/* Metrics Form Component */}
      <div className="flex justify-center">
        <MetricsForm />
      </div>
    </div>
  );
};

export default Metrics;
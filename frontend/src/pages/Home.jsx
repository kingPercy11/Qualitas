import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const cards = [
    {
      title: "Metrics Analysis",
      desc: "Analyze Halstead, Information Flow, and Live Variable metrics for your codebase.",
      icon: "📊",
      color: "from-blue-500 to-indigo-500",
      path: "/metrics",
    },
    {
      title: "Testing",
      desc: "Run and visualize your project’s unit and integration test reports.",
      icon: "🧪",
      color: "from-green-500 to-emerald-500",
      path: "/testing",
    },
    {
      title: "Quality Insights",
      desc: "Get deep insights into maintainability and overall code quality health.",
      icon: "⚙️",
      color: "from-purple-500 to-pink-500",
      path: "/quality",
    },
  ];

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-linear-to-br from-gray-100 via-blue-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 text-gray-900 dark:text-gray-100 transition-all">
      <h1 className="text-4xl font-bold mb-4"> Hi there!</h1>
      <p className="text-lg mb-10 text-gray-700 dark:text-gray-300">
        What would you like to do today?
      </p>

      {/* Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-11/12 md:w-4/5 lg:w-3/5">
        {cards.map((card, index) => (
          <div
            key={index}
            onClick={() => navigate(card.path)}
            className={`cursor-pointer bg-linear-to-br ${card.color} text-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all`}
          >
            <div className="text-5xl mb-4">{card.icon}</div>
            <h2 className="text-2xl font-semibold mb-2">{card.title}</h2>
            <p className="text-sm opacity-90">{card.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
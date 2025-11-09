import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Metrics from "./pages/Metrics";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/metrics" element={<Metrics/>} />
      </Routes>
    </Router>
  );
}

export default App;
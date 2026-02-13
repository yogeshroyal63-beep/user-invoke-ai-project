import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Landing from "./pages/Landing";
import Check from "./pages/Check";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/login";
    return null;
  }
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login First */}
        <Route path="/" element={<Login />} />

        {/* Create Account */}
        <Route path="/register" element={<Register />} />

        {/* After Auth */}
        <Route
          path="/landing"
          element={
            <ProtectedRoute>
              <Landing />
            </ProtectedRoute>
          }
        />

        {/* Main App */}
        <Route
          path="/check"
          element={
            <ProtectedRoute>
              <Check />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

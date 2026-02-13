import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Register() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  async function handleRegister(e) {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
      setMsg("Account created successfully");
      setTimeout(() => navigate("/"), 1200);
    } else {
      setMsg(data.detail || "Registration failed");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-black text-white">

      <div className="bg-gray-900/70 backdrop-blur-xl p-10 rounded-2xl w-[380px] shadow-2xl">

        <h1 className="text-3xl font-bold text-center mb-2">TrustCheck AI</h1>
        <p className="text-gray-400 text-center mb-8">
          Create Account
        </p>

        {msg && <p className="text-yellow-400 mb-3">{msg}</p>}

        <form onSubmit={handleRegister} className="space-y-4">

          <input
            type="email"
            placeholder="Email"
            className="w-full p-3 rounded-lg bg-gray-800 focus:outline-none focus:ring-2 focus:ring-green-600"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 rounded-lg bg-gray-800 focus:outline-none focus:ring-2 focus:ring-green-600"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="w-full bg-green-600 hover:bg-green-700 transition p-3 rounded-lg font-semibold">
            Register
          </button>

        </form>

        <p
          onClick={() => navigate("/")}
          className="mt-6 text-sm text-center text-blue-400 cursor-pointer"
        >
          Back to login
        </p>

      </div>
    </div>
  );
}

import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {

  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    setMsg("Password reset link sent (demo mode)");
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">

      <div className="bg-gray-900 p-10 rounded-2xl w-[380px] shadow-xl">

        <h2 className="text-2xl font-bold mb-6 text-center">
          Forgot Password
        </h2>

        {msg && <p className="text-green-400 mb-4">{msg}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="email"
            placeholder="Enter your email"
            className="w-full p-3 rounded-lg bg-gray-800 focus:ring-2 focus:ring-blue-600 outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button className="w-full bg-blue-600 p-3 rounded-lg">
            Send Reset Link
          </button>

        </form>

        <p
          onClick={() => navigate("/")}
          className="mt-6 text-sm text-blue-400 cursor-pointer text-center"
        >
          Back to Login
        </p>

      </div>
    </div>
  );
}

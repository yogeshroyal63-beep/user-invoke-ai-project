import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <nav className="w-full px-8 py-4 flex items-center justify-between bg-gradient-to-r from-[#020617] via-[#050b18] to-[#020617] border-b border-slate-800">

      {/* LEFT */}
      <div className="flex items-center gap-2 text-white font-semibold text-lg">
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
          🛡️
        </div>
        TrustCheck AI
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-6 text-slate-300">

        <Link
          to="/check"
          className="hover:text-white transition"
        >
          Check
        </Link>

        <Link
          to="/docs"
          className="hover:text-white transition"
        >
          Docs
        </Link>

        <Link
          to="/privacy"
          className="hover:text-white transition"
        >
          Privacy
        </Link>

        {/* LOGOUT BUTTON */}
        <button
          onClick={handleLogout}
          className="bg-blue-600 hover:bg-blue-700 transition px-5 py-2 rounded-lg text-white"
        >
          Logout
        </button>

      </div>

    </nav>
  );
}

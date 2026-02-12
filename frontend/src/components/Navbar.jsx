import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="w-full border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">

        {/* LOGO */}
        <Link to="/" className="flex items-center gap-2 text-white font-semibold text-lg">
          <span className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            🛡️
          </span>
          TrustCheck AI
        </Link>

        {/* LINKS */}
        <div className="hidden md:flex items-center gap-10 text-slate-300">
          <Link to="/check" className="hover:text-white">Check</Link>
          <Link to="/docs" className="hover:text-white">Docs</Link>
          <Link to="/privacy" className="hover:text-white">Privacy</Link>
        </div>

      </div>
    </nav>
  );
}

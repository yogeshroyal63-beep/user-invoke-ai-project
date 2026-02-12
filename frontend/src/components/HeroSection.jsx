import { Link } from "react-router-dom";
import shield from "../assets/shield.png";

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">

      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/40 via-slate-900 to-black z-0" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center text-center px-6 max-w-4xl mx-auto">

        {/* Badge */}
        <span className="mb-6 px-4 py-1 text-sm bg-blue-500/10 text-blue-400 rounded-full">
          ✨ AI-Powered Security Assistant
        </span>

        {/* Heading */}
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
          Ask Before You Trust
        </h1>

        {/* Subtext */}
        <p className="text-slate-400 text-lg max-w-2xl mb-10">
          Instantly check suspicious messages, links, and apps with a privacy-first AI security assistant.
        </p>

        {/* Buttons */}
        <div className="flex gap-4 mb-16">
          <Link
            to="/check"
            className="bg-blue-600 px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
          >
            Start Checking →
          </Link>

          <button className="border border-white/20 px-8 py-3 rounded-xl hover:bg-white/5 transition">
            How It Works
          </button>
        </div>

        {/* Preview Card */}
        <div className="w-full max-w-xl rounded-2xl border border-white/10 bg-gradient-to-br from-slate-800/60 to-slate-900/80 p-10">

          {/* Shield */}
          <div className="flex justify-center mb-8">
            <img
              src={shield}
              alt="Security Shield"
              className="w-28 drop-shadow-[0_0_40px_rgba(59,130,246,0.7)]"
            />
          </div>

          {/* Status Bar */}
          <div className="flex items-center gap-3 bg-black/30 border border-white/10 rounded-xl px-5 py-3">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-black font-bold">
              ✓
            </div>

            <div className="text-left">
              <p className="text-white font-medium">
                Safe Message
                <span className="ml-2 text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                  LOW RISK
                </span>
              </p>
              <p className="text-slate-400 text-sm">
                This message appears legitimate with no suspicious patterns detected.
              </p>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}

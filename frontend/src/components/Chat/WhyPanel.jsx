import { useState } from "react";

export default function WhyPanel({ explanation }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-3">
      <button
        onClick={() => setOpen(!open)}
        className="text-blue-400 text-sm"
      >
        Why is this risky?
      </button>
      {open && <p className="mt-2 text-slate-300 text-sm">{explanation}</p>}
    </div>
  );
}

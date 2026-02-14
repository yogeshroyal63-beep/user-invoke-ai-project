import { useEffect, useState } from "react";

export default function ChatSidebar({ activeId, onSelect }) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    try {
      const raw = localStorage.getItem("sessions");
      const data = raw ? JSON.parse(raw) : [];
      setSessions(Array.isArray(data) ? data : []);
    } catch {
      setSessions([]);
    }
  }, []);

  return (
    <div className="w-64 bg-[#050b18] border-r border-gray-800 p-3">

      <h2 className="text-gray-400 text-sm mb-2">History</h2>

      {sessions.map(s => (
        <div
          key={s.id}
          onClick={() => onSelect(s.id)}
          className={`p-2 rounded cursor-pointer mb-1
            ${activeId === s.id
              ? "bg-blue-600"
              : "bg-gray-800 hover:bg-gray-700"}
          `}
        >
          {s.title}
        </div>
      ))}

    </div>
  );
}

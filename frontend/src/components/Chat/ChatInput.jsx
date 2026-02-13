import { useState } from "react";

export default function ChatInput({ onSend }) {

  const [value, setValue] = useState("");

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend(value);
      setValue("");
    }
  }

  return (
    <div className="flex gap-2">
      <input
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Paste suspicious message, link, or situation..."
        className="flex-1 bg-gray-800 text-white px-4 py-3 rounded-xl outline-none"
      />
      <button
        onClick={() => {
          onSend(value);
          setValue("");
        }}
        className="bg-blue-600 px-4 rounded-xl"
      >
        ➤
      </button>
    </div>
  );
}

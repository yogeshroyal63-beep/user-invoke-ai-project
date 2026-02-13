import { useState } from "react";

export default function ChatInput({ onSend, onStop, disabled }) {

  const [value, setValue] = useState("");

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey && !disabled) {
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
        placeholder={
          disabled
            ? "TrustCheck AI is responding..."
            : "Paste suspicious message, link, or situation..."
        }
        className="flex-1 bg-gray-800 text-white px-4 py-3 rounded-xl outline-none"
      />

      {!disabled ? (
        <button
          onClick={() => {
            onSend(value);
            setValue("");
          }}
          className="bg-blue-600 px-4 rounded-xl"
        >
          ➤
        </button>
      ) : (
        <button
          onClick={onStop}
          className="bg-blue-600 hover:bg-blue-700 px-4 rounded-xl animate-pulse"
        >
          ⏹
        </button>
      )}

    </div>
  );
}

import { useState, useRef } from "react";

export default function ChatInput({ onSend, loading, onStop }) {
  const [value, setValue] = useState("");
  const fileRef = useRef(null);

  function handleSend() {
    if (!value.trim() || loading) return;
    onSend(value);
    setValue("");
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  async function handleImage(e) {
    const file = e.target.files[0];
    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/scan-image", {
        method: "POST",
        body: form
      });

      const data = await res.json();
      onSend("[Image uploaded for scan]");
    } catch {
      onSend("Image scan failed.");
    }
  }

  return (
    <div className="flex gap-2 items-center">

      {/* Image Upload */}
      <input
        ref={fileRef}
        type="file"
        accept="image/*"
        hidden
        onChange={handleImage}
      />

      <button
        onClick={() => fileRef.current.click()}
        className="bg-gray-700 px-3 py-2 rounded-lg hover:bg-gray-600"
      >
        🖼️
      </button>

      {/* Text Input */}
      <input
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Paste suspicious message, link, or situation..."
        className="flex-1 bg-gray-800 text-white px-4 py-3 rounded-xl outline-none"
      />

      {/* Send / Stop */}
      {!loading ? (
        <button
          onClick={handleSend}
          className="bg-blue-600 px-4 py-3 rounded-xl hover:bg-blue-500"
        >
          ➤
        </button>
      ) : (
        <button
          onClick={onStop}
          className="bg-blue-600 px-4 py-3 rounded-xl"
        >
          ■
        </button>
      )}
    </div>
  );
}

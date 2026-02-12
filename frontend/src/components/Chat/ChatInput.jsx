import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  function submit(e) {
    e.preventDefault();
    if (!text.trim()) return;
    onSend(text);
    setText("");
  }

  return (
    <form
      onSubmit={submit}
      className="fixed bottom-6 left-1/2 -translate-x-1/2 w-full max-w-4xl px-4"
    >
      <div className="flex bg-slate-800 border border-white/10 rounded-xl overflow-hidden">

        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste suspicious message, link, or situation..."
          className="flex-1 bg-transparent px-4 py-4 outline-none"
        />

        <button className="bg-blue-600 px-6 hover:bg-blue-700">
          ➤
        </button>

      </div>
    </form>
  );
}

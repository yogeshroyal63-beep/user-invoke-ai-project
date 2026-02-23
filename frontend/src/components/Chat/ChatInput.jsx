import { useState, useRef } from "react";
import { Paperclip } from "lucide-react";

export default function ChatInput({ onSend, loading, onStop }) {
  const [value, setValue] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const fileRef = useRef(null);

  function handleSend() {
    if (loading) return;

    if (selectedFile) {
      const isImage = selectedFile.type.startsWith("image/");

      onSend({
        type: isImage ? "image" : "file",
        file: selectedFile,
        preview,
        instruction: value.trim()
      });

      setSelectedFile(null);
      setPreview(null);
      setValue("");
      return;
    }

    if (!value.trim()) return;

    onSend(value.trim());
    setValue("");
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleFileSelect(e) {
  const file = e.target.files[0];
  if (!file) return;

  setSelectedFile(file);

  if (file.type.startsWith("image/")) {
    setPreview(URL.createObjectURL(file));
  } else {
    setPreview(null);
  }

  // 🔥 CRITICAL FIX: allow same file to be selected again
  e.target.value = "";
}

  return (
    <div className="flex flex-col gap-3">

      {selectedFile && (
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 
                        border border-slate-700 
                        p-4 rounded-2xl 
                        flex items-center justify-between 
                        shadow-lg">

          <div className="flex items-center gap-4">

            {preview ? (
              <img
                src={preview}
                alt="preview"
                className="w-16 h-16 object-cover rounded-xl border border-slate-600 shadow"
              />
            ) : (
              <div className="bg-slate-700 px-4 py-2 rounded-xl text-sm text-gray-300 shadow">
                {selectedFile.name}
              </div>
            )}

            <div className="flex flex-col">
              <span className="text-sm text-gray-200 font-medium">
                {selectedFile.name}
              </span>
              <span className="text-xs text-gray-500">
                {(selectedFile.size / 1024).toFixed(1)} KB
              </span>
            </div>

          </div>

          <button
            onClick={() => {
              setSelectedFile(null);
              setPreview(null);
            }}
            className="text-red-400 hover:text-red-300 text-sm font-medium"
          >
            Remove
          </button>

        </div>
      )}

      <div className="flex gap-3 items-center">

        <input
          ref={fileRef}
          type="file"
          hidden
          onChange={handleFileSelect}
        />

        <button
          onClick={() => fileRef.current.click()}
          className="bg-slate-700 p-3 rounded-2xl hover:bg-slate-600 transition shadow-md"
        >
          <Paperclip size={18} />
        </button>

        <input
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKey}
          placeholder={
            selectedFile
              ? "Add instruction for this file (optional)..."
              : "Paste suspicious message, link, or upload file..."
          }
          className="flex-1 bg-slate-800 text-white px-5 py-3 rounded-2xl outline-none shadow-inner"
        />

        {!loading ? (
          <button
            onClick={handleSend}
            className="bg-gradient-to-br from-blue-600 to-blue-500 
                       px-6 py-3 rounded-2xl 
                       hover:from-blue-500 hover:to-blue-400 
                       transition shadow-md"
          >
            ➤
          </button>
        ) : (
          <button
            onClick={onStop}
            className="bg-gradient-to-br from-blue-600 to-blue-500 
                       px-6 py-3 rounded-2xl 
                       hover:from-red-500 hover:to-red-400 
                       transition shadow-md text-white text-lg"
          >
            ■
          </button>
        )}

      </div>
    </div>
  );
}
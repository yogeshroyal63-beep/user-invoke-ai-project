import { useState, useRef } from "react";

export default function ChatInput({ onSend, loading, onStop }) {
  const [value, setValue] = useState("");
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const fileRef = useRef(null);

  function handleSend() {
    if (loading) return;

    // IMAGE SEND
    if (selectedImage) {
      onSend({
        type: "image",
        file: selectedImage,
        preview: preview,
        instruction: value.trim()
      });

      setSelectedImage(null);
      setPreview(null);
      setValue("");
      return;
    }

    // NORMAL TEXT SEND
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

  function handleImageSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    setSelectedImage(file);
    setPreview(URL.createObjectURL(file));
  }

  return (
    <div className="flex flex-col gap-2">

      {/* IMAGE PREVIEW */}
      {preview && (
        <div className="relative w-40">
          <img
            src={preview}
            alt="preview"
            className="rounded-lg border border-gray-700"
          />
          <button
            onClick={() => {
              setSelectedImage(null);
              setPreview(null);
            }}
            className="absolute top-1 right-1 bg-black bg-opacity-70 text-white rounded-full px-2"
          >
            ✕
          </button>
        </div>
      )}

      <div className="flex gap-2 items-center">

        {/* FILE INPUT */}
        <input
          ref={fileRef}
          type="file"
          accept="image/*"
          hidden
          onChange={handleImageSelect}
        />

        <button
          onClick={() => fileRef.current.click()}
          className="bg-gray-700 px-3 py-2 rounded-lg hover:bg-gray-600"
        >
          🖼️
        </button>

        {/* TEXT INPUT */}
        <input
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKey}
          placeholder={
            selectedImage
              ? "Add instruction for this image (optional)..."
              : "Paste suspicious message, link, or situation..."
          }
          className="flex-1 bg-gray-800 text-white px-4 py-3 rounded-xl outline-none"
        />

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
    </div>
  );
}

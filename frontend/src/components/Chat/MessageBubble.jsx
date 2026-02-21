export default function MessageBubble({ message }) {

  if (!message) return null;

  const isUser = message.role === "user";
  const isScam =
    message.mode === "scam" || message.type === "scam";

  // ================= USER =================
  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-md space-y-2">

          {message.mode === "image" && message.imageUrl && (
            <img
              src={message.imageUrl}
              alt="uploaded"
              className="rounded-xl border border-gray-700"
            />
          )}

          {message.text && (
            <div className="bg-blue-600 px-4 py-2 rounded-xl break-words">
              {message.text}
            </div>
          )}

        </div>
      </div>
    );
  }

  // ================= SCAM =================
  if (isScam) {

    const risk = message.risk || "HIGH";
    const category = message.category || "Scam";
    const confidence = message.confidence ?? 90;
    const explanation =
      message.explanation || message.text || "Suspicious content detected.";
    const tips = Array.isArray(message.tips) ? message.tips : [];

    return (
      <div className="flex justify-start">
        <div className="bg-slate-800 border border-red-600 p-5 rounded-xl max-w-xl">

          <div className="flex gap-2 items-center mb-3 flex-wrap">

            <span className="bg-red-600 px-2 py-1 rounded text-xs font-bold">
              {risk} RISK
            </span>

            <span className="bg-yellow-500 text-black px-2 py-1 rounded text-xs font-bold">
              {category}
            </span>

            <span className="bg-blue-600 px-2 py-1 rounded text-xs font-bold">
              {confidence}% Confidence
            </span>

          </div>

          <p className="text-gray-200 mb-3 break-words">
            {explanation}
          </p>

          {tips.length > 0 && (
            <>
              <h4 className="font-semibold mb-1">Safety Tips:</h4>
              <ul className="list-disc ml-5 text-gray-300 space-y-1">
                {tips.map((t, i) => (
                  <li key={i}>{t}</li>
                ))}
              </ul>
            </>
          )}

        </div>
      </div>
    );
  }

  // ================= NORMAL CHAT =================
  return (
    <div className="flex justify-start">
      <div className="bg-gray-700 px-4 py-2 rounded-xl max-w-md break-words">
        {message.text || message.reply || ""}
      </div>
    </div>
  );
}
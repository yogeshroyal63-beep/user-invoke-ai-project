export default function MessageBubble({ message }) {
  if (!message) return null;

  const isUser = message.role === "user";
  const isScam =
    message.mode === "scam" || message.type === "scam";

  // ================= USER =================
  if (isUser) {
    return (
      <div className="flex justify-end w-full">
        <div className="max-w-lg space-y-3">

          {message.mode === "image" && message.imageUrl && (
            <img
              src={message.imageUrl}
              alt="uploaded"
              className="rounded-2xl border border-gray-700 shadow-md"
            />
          )}

          {message.text && (
            <div className="bg-gradient-to-br from-blue-600 to-blue-500 
                            px-5 py-3 rounded-2xl 
                            shadow-md 
                            text-white 
                            break-words">
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
      <div className="flex justify-start w-full">
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 
                        border border-red-500 
                        p-6 
                        rounded-2xl 
                        max-w-2xl 
                        shadow-xl 
                        space-y-4">

          <div className="flex gap-2 items-center flex-wrap">

            <span className="bg-red-600 px-3 py-1 rounded-full text-xs font-semibold shadow">
              {risk} RISK
            </span>

            <span className="bg-yellow-400 text-black px-3 py-1 rounded-full text-xs font-semibold shadow">
              {category}
            </span>

            <span className="bg-blue-500 px-3 py-1 rounded-full text-xs font-semibold shadow">
              {confidence}% Confidence
            </span>

          </div>

          <p className="text-gray-200 leading-relaxed break-words">
            {explanation}
          </p>

          {tips.length > 0 && (
            <div className="bg-slate-700/40 p-4 rounded-xl">
              <h4 className="font-semibold mb-2 text-gray-100">
                Safety Tips
              </h4>
              <ul className="list-disc ml-5 text-gray-300 space-y-1">
                {tips.map((t, i) => (
                  <li key={i}>{t}</li>
                ))}
              </ul>
            </div>
          )}

        </div>
      </div>
    );
  }

  // ================= NORMAL CHAT =================
  return (
    <div className="flex justify-start w-full">
      <div className="bg-slate-700 
                      px-5 py-3 
                      rounded-2xl 
                      max-w-lg 
                      shadow-md 
                      text-gray-100 
                      break-words">
        {message.text || message.reply || ""}
      </div>
    </div>
  );
}
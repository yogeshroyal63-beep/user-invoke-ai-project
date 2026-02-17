export default function MessageBubble({ message }) {

  if (!message) return null;

  // ================= USER =================
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="bg-blue-600 px-4 py-2 rounded-xl max-w-md">
          {message.text}
        </div>
      </div>
    );
  }

  // ================= SCAM =================
  if (message.mode === "scam") {

    const risk = message.risk || "HIGH";
    const category = message.category || "Scam";
    const confidence = message.confidence ?? 90;
    const explanation =
      message.explanation || "Suspicious content detected.";
    const tips = Array.isArray(message.tips) ? message.tips : [];

    return (
      <div className="bg-slate-800 border border-gray-700 p-5 rounded-xl max-w-xl">

        <div className="flex gap-2 items-center mb-2">
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

        <p className="text-gray-200 mb-3">
          {explanation}
        </p>

        {tips.length > 0 && (
          <>
            <h4 className="font-semibold mb-1">Why is this risky?</h4>

            <ul className="list-disc ml-5 text-gray-300">
              {tips.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          </>
        )}

      </div>
    );
  }

  // ================= NORMAL CHAT =================
  return (
    <div className="bg-gray-700 px-4 py-2 rounded-xl max-w-md">
      {message.text}
    </div>
  );
}

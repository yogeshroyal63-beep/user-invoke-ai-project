export default function MessageBubble({ message }) {
  if (!message) return null;

  const isUser = message.role === "user";
  const isScam = message.mode === "scam" || message.type === "scam";

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
            <div
              className="bg-gradient-to-br from-blue-600 to-blue-500
                         px-5 py-3 rounded-2xl
                         shadow-md text-white break-words"
            >
              {message.text}
            </div>
          )}

        </div>
      </div>
    );
  }

  // ================= SECURITY CARD =================
  if (isScam) {

    const risk = message.risk || "LOW";
    const category = message.category || "Security Analysis";
    const confidence = message.confidence ?? 75;
    const explanation =
      message.explanation || "Security analysis completed.";
    const tips = Array.isArray(message.tips) ? message.tips : [];
    const signals = message.signals || {};
    const followUp = message.follow_up || null;

    const riskColor =
      risk === "HIGH"
        ? "bg-red-600"
        : risk === "MEDIUM"
        ? "bg-yellow-500 text-black"
        : "bg-blue-600";

    const borderColor =
      risk === "HIGH"
        ? "border-red-500"
        : risk === "MEDIUM"
        ? "border-yellow-500"
        : "border-blue-500";

    return (
      <div className="flex justify-start w-full">
        <div
          className={`bg-gradient-to-br from-slate-800 to-slate-900
                      ${borderColor} border
                      p-6 rounded-2xl
                      max-w-2xl
                      shadow-xl space-y-5`}
        >

          {/* Top Badges */}
          <div className="flex gap-2 items-center flex-wrap">

            <span
              className={`${riskColor}
                         px-3 py-1 rounded-full
                         text-xs font-semibold shadow`}
            >
              {risk} RISK
            </span>

            <span
              className="bg-slate-600
                         px-3 py-1 rounded-full
                         text-xs font-semibold shadow"
            >
              {category}
            </span>

            <span
              className="bg-slate-700
                         px-3 py-1 rounded-full
                         text-xs font-semibold shadow"
            >
              {confidence}% Confidence
            </span>

          </div>

          {/* Explanation */}
          <p className="text-gray-200 leading-relaxed break-words">
            {explanation}
          </p>

          {/* Detected Indicators (HIDE ONLY IF LOW) */}
          {risk !== "LOW" &&
            signals &&
            Object.keys(signals).length > 0 && (
              <div className="bg-slate-700/40 p-4 rounded-xl">
                <h4 className="font-semibold mb-2 text-gray-100">
                  Detected Indicators
                </h4>
                <ul className="list-disc ml-5 text-gray-300 space-y-1">
                  {Object.entries(signals).map(([key, value], index) => {

                    if (!value) return null;

                    if (Array.isArray(value) && value.length === 0) return null;

                    if (Array.isArray(value)) {
                      return value.map((v, i) => (
                        <li key={`${index}-${i}`}>{v}</li>
                      ));
                    }

                    if (typeof value === "boolean" && value === true) {
                      return <li key={index}>{key}</li>;
                    }

                    if (typeof value === "number") {
                      return <li key={index}>{key}: {value}</li>;
                    }

                    return null;
                  })}
                </ul>
              </div>
            )}

          {/* Safety Tips */}
          {tips.length > 0 && (
            <div className="bg-slate-700/40 p-4 rounded-xl">
              <h4 className="font-semibold mb-2 text-gray-100">
                Safety Tips
              </h4>
              <ul className="list-disc ml-5 text-gray-300 space-y-1">
                {tips.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Follow Up Block */}
          {followUp && (
            <div className="bg-blue-700/30 p-4 rounded-xl border border-blue-500">
              <p className="text-blue-200">{followUp}</p>
            </div>
          )}

        </div>
      </div>
    );
  }

  // ================= NORMAL CHAT =================
  return (
    <div className="flex justify-start w-full">
      <div
        className="bg-slate-700
                   px-5 py-3 rounded-2xl
                   max-w-lg shadow-md
                   text-gray-100 break-words"
      >
        {message.text || message.reply || ""}
      </div>
    </div>
  );
}
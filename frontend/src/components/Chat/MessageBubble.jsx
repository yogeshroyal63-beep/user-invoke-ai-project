export default function MessageBubble({ message }) {

  const base =
    "animate-fade-in transition-all duration-300";

  if (message.role === "user") {
    return (
      <div className={`flex justify-end ${base}`}>
        <div className="bg-blue-600 px-4 py-2 rounded-xl max-w-md">
          {message.text}
        </div>
      </div>
    );
  }

  if (message.mode === "chat") {
    return (
      <div className={`flex justify-start ${base}`}>
        <div className="bg-gray-700 px-4 py-2 rounded-xl max-w-md">
          {message.text}
        </div>
      </div>
    );
  }

  if (message.mode === "scam") {
    return (
      <div className={`bg-gray-800 p-4 rounded-xl border border-gray-600 max-w-lg ${base}`}>
        <span
          className={`px-3 py-1 rounded-full text-xs font-bold
            ${message.risk === "HIGH" ? "bg-red-600" :
              message.risk === "MEDIUM" ? "bg-yellow-500 text-black" :
              "bg-green-600"}
          `}
        >
          {message.risk} RISK
        </span>

        <p className="mt-2">{message.explanation}</p>

        {message.tips?.length > 0 && (
          <>
            <p className="mt-3 font-semibold">Why is this risky?</p>
            <ul className="list-disc ml-5 text-slate-300">
              {message.tips.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          </>
        )}
      </div>
    );
  }

  return null;
}

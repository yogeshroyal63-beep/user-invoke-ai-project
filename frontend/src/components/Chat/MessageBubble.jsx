export default function MessageBubble({ message }) {

  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="bg-blue-600 px-4 py-2 rounded-xl max-w-md">
          {message.text}
        </div>
      </div>
    );
  }

  if (message.mode === "scam") {
    return (
      <div className="bg-slate-800 border border-gray-700 p-5 rounded-xl max-w-xl">

        <div className="flex gap-2 items-center mb-2">
          <span className="bg-red-600 px-2 py-1 rounded text-xs font-bold">
            {message.risk} RISK
          </span>

          <span className="bg-yellow-500 text-black px-2 py-1 rounded text-xs font-bold">
            {message.category}
          </span>

          <span className="bg-blue-600 px-2 py-1 rounded text-xs font-bold">
            {message.confidence}% Confidence
          </span>
        </div>

        <p className="text-gray-200 mb-3">
          {message.explanation}
        </p>

        <h4 className="font-semibold mb-1">Why is this risky?</h4>

        <ul className="list-disc ml-5 text-gray-300">
          {message.tips.map((t, i) => (
            <li key={i}>{t}</li>
          ))}
        </ul>
      </div>
    );
  }

  return (
    <div className="bg-gray-700 px-4 py-2 rounded-xl max-w-md">
      {message.text}
    </div>
  );
}

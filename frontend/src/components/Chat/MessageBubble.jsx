import RiskBadge from "./RiskBadge";
import WhyPanel from "./WhyPanel";

export default function MessageBubble({ data }) {

  if (data.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="bg-blue-600 text-white px-5 py-3 rounded-xl max-w-lg">
          {data.text}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 border border-white/10 p-6 rounded-xl max-w-2xl">

      <RiskBadge level={data.risk} />

      <p className="mt-4 text-slate-100">
        {data.explanation}
      </p>

      <WhyPanel />

      {data.tips?.length > 0 && (
        <ul className="list-disc ml-5 mt-3 text-slate-300">
          {data.tips.map((tip, i) => (
            <li key={i}>{tip}</li>
          ))}
        </ul>
      )}

    </div>
  );
}

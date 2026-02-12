import Shield from "../../assets/shield.png";

export default function RiskBadge({ level }) {

  const colors = {
    "LOW RISK": "bg-green-500/20 text-green-400",
    "MEDIUM RISK": "bg-yellow-500/20 text-yellow-400",
    "HIGH RISK": "bg-red-500/20 text-red-400",
    "UNKNOWN": "bg-slate-500/20 text-slate-300"
  };

  return (
    <div className={`flex items-center gap-2 px-4 py-2 rounded-full w-fit ${colors[level]}`}>
      <img
        src={Shield}
        className="w-5 h-5"
        alt="shield"
      />
      <span className="font-semibold text-sm">
        {level}
      </span>
    </div>
  );
}

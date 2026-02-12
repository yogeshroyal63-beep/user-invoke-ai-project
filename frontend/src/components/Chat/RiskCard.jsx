export default function RiskBadge({ level }) {
  const colors = {
    LOW: "bg-green-600",
    MEDIUM: "bg-yellow-500",
    HIGH: "bg-red-600",
    ERROR: "bg-gray-600",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${colors[level]}`}
    >
      {level} RISK
    </span>
  );
}

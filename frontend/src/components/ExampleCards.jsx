export default function ExampleCards() {
  const examples = [
    ["Suspicious Email", "Your account has been suspended"],
    ["Unknown Link", "bit.ly/verify-bank"],
    ["Payment Request", "Confirm ₹500 immediately"]
  ];

  return (
    <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-4 px-6 mb-10">
      {examples.map((e, i) => (
        <div key={i} className="bg-white/5 border border-white/10 rounded-xl p-4">
          <h3 className="font-semibold">{e[0]}</h3>
          <p className="text-slate-400 text-sm mt-1">{e[1]}</p>
        </div>
      ))}
    </div>
  );
}

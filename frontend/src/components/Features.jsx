export default function ExampleCards() {
  const features = [
    {
      title: "Scam Message Detection",
      desc: "AI-powered analysis with zero background monitoring.",
    },
    {
      title: "Phishing Link Analysis",
      desc: "AI-powered analysis with zero background monitoring.",
    },
    {
      title: "Payment Fraud Detection",
      desc: "AI-powered analysis with zero background monitoring.",
    },
    {
      title: "Privacy-First AI",
      desc: "AI-powered analysis with zero background monitoring.",
    },
  ];

  return (
    <section className="py-28">
      <div className="max-w-7xl mx-auto px-6">

        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {features.map((f, i) => (
            <div
              key={i}
              className="bg-slate-800/60 backdrop-blur-md p-8 rounded-2xl border border-white/10
                         hover:border-blue-500/30 transition"
            >
              <h3 className="text-lg font-semibold mb-4 leading-snug">
                {f.title}
              </h3>

              <p className="text-slate-400 text-sm leading-relaxed max-w-[260px]">
                {f.desc}
              </p>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}

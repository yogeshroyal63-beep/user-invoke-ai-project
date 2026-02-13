export default function ExampleCards({ onSelect }) {

  const examples = [
    "Your account has been suspended",
    "bit.ly/verify-bank",
    "Confirm ₹500 immediately"
  ];

  function handleClick(text) {
    window.dispatchEvent(
      new CustomEvent("exampleMessage", { detail: text })
    );

    onSelect();   // 🔥 THIS triggers landing → chat transition
  }

  return (
    <div className="grid md:grid-cols-3 gap-4 mb-10">

      {examples.map((ex, i) => (
        <div
          key={i}
          onClick={() => handleClick(ex)}
          className="cursor-pointer bg-slate-800 p-4 rounded-xl hover:bg-slate-700 transition"
        >
          <p className="font-semibold">{ex}</p>
        </div>
      ))}

    </div>
  );
}

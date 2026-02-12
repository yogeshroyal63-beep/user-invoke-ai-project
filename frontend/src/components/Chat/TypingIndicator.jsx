export default function TypingIndicator() {
  return (
    <div className="flex gap-1 text-slate-400">
      <span className="animate-bounce">.</span>
      <span className="animate-bounce delay-150">.</span>
      <span className="animate-bounce delay-300">.</span>
    </div>
  );
}

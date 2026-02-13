import { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

export default function ChatContainer() {

  const [started, setStarted] = useState(false);
  const [typing, setTyping] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      mode: "chat",
      text: "Hi 👋 I'm TrustCheck AI. Send any message or link and I'll analyze it."
    }
  ]);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  async function sendMessage(text) {
    if (!text || !text.trim()) return;

    setStarted(true);

    setMessages(prev => [...prev, { role: "user", text }]);
    setTyping(true);

    try {
      const res = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      setTyping(false);

      // SAFE NORMAL CHAT
      if (data?.type === "chat") {
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: typeof data.reply === "string"
              ? data.reply
              : data.reply?.reply || "Hello."
          }
        ]);
        return;
      }

      // SAFE SCAM
      if (data?.type === "scam") {
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "scam",
            risk: data.risk || "LOW",
            explanation: data.explanation || "No explanation provided.",
            tips: Array.isArray(data.tips) ? data.tips : []
          }
        ]);
        return;
      }

      // FALLBACK
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          mode: "chat",
          text: "Unexpected response."
        }
      ]);

    } catch {
      setTyping(false);
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          mode: "chat",
          text: "Server error."
        }
      ]);
    }
  }

  return (
    <div className="h-screen bg-black text-white flex flex-col">

      {!started && (
        <div className="flex-1 flex flex-col items-center justify-center gap-8">

          <h1 className="text-4xl font-bold">Security Check Assistant</h1>

          <div className="flex gap-4">

            <Card
              title="Suspicious Email"
              text="Your account has been suspended"
              onClick={() => sendMessage("Your account has been suspended")}
            />

            <Card
              title="Unknown Link"
              text="bit.ly/verify-bank"
              onClick={() => sendMessage("bit.ly/verify-bank")}
            />

            <Card
              title="Payment Request"
              text="Confirm ₹500 immediately"
              onClick={() => sendMessage("Confirm ₹500 immediately")}
            />

          </div>

          <div className="w-[600px]">
            <ChatInput onSend={sendMessage} />
          </div>

        </div>
      )}

      {started && (
        <>
          <div className="flex-1 overflow-y-auto p-6 flex justify-center">
            <div className="w-full max-w-3xl space-y-4">
              {messages.map((m, i) => (
                <MessageBubble key={i} message={m} />
              ))}

              {typing && <TypingIndicator />}

              <div ref={bottomRef}></div>
            </div>
          </div>

          <div className="p-4 border-t border-gray-800 flex justify-center">
            <div className="w-full max-w-3xl">
              <ChatInput onSend={sendMessage} />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function Card({ title, text, onClick }) {
  return (
    <div
      onClick={onClick}
      className="cursor-pointer bg-gray-800 hover:bg-gray-700 px-6 py-4 rounded-xl w-64 transition"
    >
      <h3 className="font-semibold">{title}</h3>
      <p className="text-gray-400 text-sm mt-1">{text}</p>
    </div>
  );
}

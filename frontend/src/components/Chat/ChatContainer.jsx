import { useState } from "react";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";

export default function ChatContainer() {
  const [messages, setMessages] = useState([]);

  async function sendMessage(text) {
    setMessages(prev => [...prev, { role: "user", text }]);

    const res = await fetch("http://localhost:8000/api/analyze"
, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();

    setMessages(prev => [
      ...prev,
      {
        role: "ai",
        chat: data.chat_reply,
        risk: data.risk,
        explanation: data.explanation,
        advice: data.tips
      }
    ]);
  }

  return (
    <div className="max-w-4xl mx-auto h-[80vh] flex flex-col">

      <div className="flex-1 overflow-y-auto space-y-6 px-2 py-4">
        {messages.map((m, i) => (
          <MessageBubble key={i} data={m} />
        ))}
      </div>

      <ChatInput onSend={sendMessage} />
    </div>
  );
}

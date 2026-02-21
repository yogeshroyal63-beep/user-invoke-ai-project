import { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

export default function ChatContainer() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      mode: "chat",
      text: "Hi 👋 I'm TrustCheck AI. Send any message, link, file, or image."
    }
  ]);

  const [typing, setTyping] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  async function sendMessage(payload) {

    if (typing) return;

    // ================= TEXT MESSAGE =================
    if (typeof payload === "string") {

      const cleanText = payload.trim();
      if (!cleanText) return;

      const userMessage = {
        role: "user",
        mode: "chat",
        text: cleanText
      };

      const updatedMessages = [...messages, userMessage];
      setMessages(updatedMessages);
      setTyping(true);

      try {

        const historyPayload = updatedMessages.map(m => ({
          role: m.role,
          text: m.text || "[Image]"
        }));

        const res = await fetch("http://127.0.0.1:8000/api/scan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: cleanText,
            history: historyPayload
          })
        });

        const data = await res.json();
        setTyping(false);

        if (data?.type === "scam") {
          setMessages(prev => [
            ...prev,
            {
              role: "assistant",
              mode: "scam",
              risk: data.risk,
              category: data.category,
              confidence: data.confidence,
              explanation: data.explanation,
              tips: data.tips
            }
          ]);
          return;
        }

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: data.reply || "Hello 👋"
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

      return;
    }

    // ================= IMAGE MESSAGE =================
    if (payload?.type === "image") {

      const imageMessage = {
        role: "user",
        mode: "image",
        imageUrl: payload.preview,
        text: payload.instruction || null
      };

      setMessages(prev => [...prev, imageMessage]);

      if (!payload.instruction || !payload.instruction.trim()) {
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: "What would you like me to analyze in this image?"
          }
        ]);
        return;
      }

      setTyping(true);

      try {

        const historyPayload = [
          ...messages.map(m => ({
            role: m.role,
            text: m.text || "[Image]"
          })),
          { role: "user", text: payload.instruction }
        ];

        const res = await fetch("http://127.0.0.1:8000/api/scan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: payload.instruction,
            history: historyPayload
          })
        });

        const data = await res.json();
        setTyping(false);

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: data.reply || "Image analyzed."
          }
        ]);

      } catch {
        setTyping(false);
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: "Image analysis failed."
          }
        ]);
      }

      return;
    }
  }

  return (
    <div className="h-screen bg-black text-white flex flex-col">

      <div className="flex-1 overflow-y-auto p-6 flex justify-center">
        <div className="w-full max-w-3xl space-y-4">
          {messages.map((m, i) => (
            <MessageBubble key={i} message={m} />
          ))}
          {typing && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </div>

      <div className="p-4 border-t border-gray-800 flex justify-center">
        <div className="w-full max-w-3xl">
          <ChatInput
            onSend={sendMessage}
            loading={typing}
            onStop={() => setTyping(false)}
          />
        </div>
      </div>

    </div>
  );
}

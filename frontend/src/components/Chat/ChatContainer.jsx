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

  async function sendMessage(text) {

    if (!text || !text.trim() || typing) return;

    const cleanText = text.trim();

    const userMessage = {
      role: "user",
      mode: "chat",
      text: cleanText
    };

    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);
    setTyping(true);

    try {

      // ✅ SEND CLEAN HISTORY STRUCTURE ONLY
      const historyPayload = updatedMessages.map(m => ({
        role: m.role,
        text: m.mode === "chat"
          ? m.text
          : m.explanation || ""
      }));

      const res = await fetch("http://127.0.0.1:8000/api/scan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: cleanText,
          history: historyPayload,
          email: localStorage.getItem("email") || null
        })
      });

      if (!res.ok) {
        throw new Error("Backend error");
      }

      const data = await res.json();
      console.log("API RESPONSE:", data);

      setTyping(false);

      // 🔴 SCAM RESPONSE
      if (data?.type === "scam") {

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "scam",
            risk: data.risk || "HIGH",
            category: data.category || "Scam",
            confidence: typeof data.confidence === "number" ? data.confidence : 90,
            explanation: data.explanation || "",
            tips: Array.isArray(data.tips) ? data.tips : []
          }
        ]);

        return;
      }

      // 🟢 NORMAL CHAT RESPONSE
      if (data?.type === "chat") {

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: data.reply || "Hello 👋"
          }
        ]);

        return;
      }

      // 🟡 UNKNOWN FORMAT
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          mode: "chat",
          text: "Unexpected response format."
        }
      ]);

    } catch (err) {

      console.error("Frontend error:", err);
      setTyping(false);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          mode: "chat",
          text: "Server error. Please try again."
        }
      ]);
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

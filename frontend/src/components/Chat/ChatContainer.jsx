import { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

const API_BASE = "http://127.0.0.1:8000";
const API_KEY = "trustcheck-secret";

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

    // ================= TEXT =================
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

        const res = await fetch(`${API_BASE}/api/scan`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
          },
          body: JSON.stringify({
            message: cleanText,
            history: historyPayload,
            image_base64: null
          })
        });

        const data = await res.json();
        setTyping(false);

        if (!res.ok) {
          throw new Error(data.error || "Request failed");
        }

        if (data?.type === "scam") {
          setMessages(prev => [
            ...prev,
            {
              role: "assistant",
              mode: "scam",
              ...data
            }
          ]);
          return;
        }

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: data.reply || "No response."
          }
        ]);
      } catch (error) {
        setTyping(false);
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: `Error: ${error.message}`
          }
        ]);
      }

      return;
    }

    // ================= IMAGE =================
    if (payload?.type === "image") {
      const imageMessage = {
        role: "user",
        mode: "image",
        imageUrl: payload.preview,
        text: payload.instruction || null
      };

      setMessages(prev => [...prev, imageMessage]);

      if (!payload.file) return;

      setTyping(true);

      try {
        const base64 = await toBase64(payload.file);

        const historyPayload = [...messages, imageMessage].map(m => ({
          role: m.role,
          text: m.text || "[Image]"
        }));

        const res = await fetch(`${API_BASE}/api/scan`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
          },
          body: JSON.stringify({
            message: payload.instruction || "Analyze this image",
            history: historyPayload,
            image_base64: base64.split(",")[1]
          })
        });

        const data = await res.json();
        setTyping(false);

        if (!res.ok) {
          throw new Error(data.error || "Image scan failed");
        }

        if (data?.type === "scam") {
          setMessages(prev => [
            ...prev,
            {
              role: "assistant",
              mode: "scam",
              ...data
            }
          ]);
          return;
        }

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: data.reply || "Image analyzed."
          }
        ]);
      } catch (error) {
        setTyping(false);
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            mode: "chat",
            text: `Error: ${error.message}`
          }
        ]);
      }
    }
  }

  function toBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
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
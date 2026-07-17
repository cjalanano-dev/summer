import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [status, setStatus] = useState("checking");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then(() => setStatus("connected"))
      .catch(() => setStatus("error"));
  }, []);

  const handleSend = async (text) => {
    const updatedMessages = [...messages, { role: "user", content: text }];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: updatedMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.body) {
        throw new Error("No response stream");
      }

      // Add placeholder assistant message
      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        // Save the last incomplete line back to the buffer
        buffer = lines.pop() || "";

        for (const line of lines) {
          const cleanLine = line.trim();
          if (cleanLine.startsWith("data: ")) {
            try {
              const payload = JSON.parse(cleanLine.substring(6));
              if (payload.content) {
                setMessages((prev) => {
                  const copy = [...prev];
                  const last = copy[copy.length - 1];
                  if (last && last.role === "assistant") {
                    last.content += payload.content;
                  }
                  return copy;
                });
              } else if (payload.error) {
                console.error("SSE Error:", payload.error);
              }
            } catch {
              // Ignore split JSON chunks
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: Failed to fetch response from Summer." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="h-screen w-full flex bg-gray-950 text-white overflow-hidden">
      <Sidebar status={status} onNewChat={handleNewChat} />
      <div className="flex-1 flex flex-col h-full relative">
        <TopBar status={status} />
        <ChatWindow messages={messages} />
        <InputBox onSend={handleSend} disabled={loading || status !== "connected"} />
      </div>
    </div>
  );
}

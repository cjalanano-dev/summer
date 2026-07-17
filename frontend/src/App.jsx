import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";

const API_BASE = "http://localhost:8000";

function mergeStreamChunk(existing, chunk) {
  if (!chunk) return existing;
  if (!existing) return chunk;

  if (chunk.startsWith(existing)) {
    return existing + chunk.slice(existing.length);
  }

  if (existing.startsWith(chunk)) {
    return existing;
  }

  return existing + chunk;
}

export default function App() {
  const [status, setStatus] = useState("checking");
  const [models, setModels] = useState([]);
  const [currentModel, setCurrentModel] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modelLoading, setModelLoading] = useState(true);

  useEffect(() => {
    async function loadBootstrapData() {
      try {
        const [healthRes, modelsRes] = await Promise.all([
          fetch(`${API_BASE}/health`),
          fetch(`${API_BASE}/models`),
        ]);

        if (!healthRes.ok || !modelsRes.ok) {
          throw new Error("Bootstrap request failed");
        }

        const modelData = await modelsRes.json();
        const availableModels = modelData.models || [];
        const nextModel = modelData.currentModel || availableModels[0] || "";

        setModels(availableModels);
        setCurrentModel(nextModel);
        setStatus("connected");
      } catch {
        setStatus("error");
      } finally {
        setModelLoading(false);
      }
    }

    loadBootstrapData();
  }, []);

  const handleModelChange = async (model) => {
    setCurrentModel(model);

    try {
      await fetch(`${API_BASE}/models/select`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ model }),
      });
    } catch (err) {
      console.error(err);
    }
  };

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
          model: currentModel || undefined,
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
                  const lastIndex = copy.length - 1;
                  const last = copy[lastIndex];
                  if (last && last.role === "assistant") {
                    copy[lastIndex] = {
                      ...last,
                      content: mergeStreamChunk(last.content, payload.content),
                    };
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
    <div className="h-screen w-full overflow-hidden bg-[#0b0f14] text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(148,163,184,0.12),_transparent_30%),radial-gradient(circle_at_top_right,_rgba(59,130,246,0.12),_transparent_24%),linear-gradient(180deg,_rgba(15,23,42,0.92),_rgba(9,12,18,1))]" />
      <div className="relative h-full w-full flex">
      <Sidebar status={status} onNewChat={handleNewChat} />
      <div className="flex-1 flex flex-col h-full min-w-0">
        <TopBar
          status={status}
          currentModel={currentModel}
          models={models}
          modelLoading={modelLoading}
          onModelChange={handleModelChange}
        />
        <ChatWindow messages={messages} />
        <InputBox
          onSend={handleSend}
          disabled={loading || status !== "connected"}
          currentModel={currentModel}
          models={models}
          modelLoading={modelLoading}
          onModelChange={handleModelChange}
        />
      </div>
      </div>
    </div>
  );
}

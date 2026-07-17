import React, { useRef, useEffect } from "react";
import Message from "./Message";

export default function ChatWindow({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto bg-gray-950">
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-center p-8">
          <div className="w-16 h-16 rounded-full bg-blue-900/30 flex items-center justify-center text-3xl mb-4 border border-blue-800/30">
            ☀️
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Welcome to Summer</h3>
          <p className="text-gray-400 max-w-sm text-sm">
            I am a context-aware AI assistant equipped with symbolic memory and workspace intelligence. How can I help you today?
          </p>
        </div>
      ) : (
        <div className="pb-8">
          {messages.map((msg, idx) => (
            <Message
              key={idx}
              role={msg.role}
              content={msg.content}
              toolCalls={msg.toolCalls}
            />
          ))}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
}

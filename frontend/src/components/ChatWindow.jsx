import { useRef, useEffect } from "react";
import Message from "./Message";

export default function ChatWindow({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto">
      {messages.length === 0 ? (
        <div className="mx-auto flex h-full max-w-6xl items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
          <div className="w-full max-w-2xl rounded-[2rem] border border-white/10 bg-white/[0.03] p-8 text-center shadow-2xl shadow-black/20 backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-2xl">
              ☀️
            </div>
            <h3 className="text-2xl font-semibold tracking-tight text-white">Welcome to Summer</h3>
            <p className="mt-3 text-sm leading-6 text-gray-400">
              A minimal local assistant for coding, context, and memory-aware conversations.
            </p>
          </div>
        </div>
      ) : (
        <div className="mx-auto w-full max-w-6xl pb-8 pt-4 sm:px-6 lg:px-8">
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

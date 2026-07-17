import { useRef, useEffect } from "react";
import { useChatStore } from "../../store/chatStore";
import Message from "./Message";

export default function ChatWindow() {
  const messages = useChatStore((s) => s.messages);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto">
      {messages.length === 0 ? (
        <div className="mx-auto flex h-full max-w-6xl items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
          <div className="w-full max-w-lg rounded-2xl border border-neutral-800 bg-neutral-950 p-8 text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl border border-neutral-700 bg-neutral-900 text-lg font-light text-white">
              S
            </div>
            <h3 className="text-lg font-semibold tracking-tight text-white">Summer</h3>
            <p className="mt-2 text-sm leading-6 text-neutral-600">
              A minimal local assistant for coding, context, and memory-aware conversations.
            </p>
          </div>
        </div>
      ) : (
        <div className="mx-auto w-full max-w-6xl pb-8 pt-2 sm:px-6 lg:px-8">
          {messages.map((msg, idx) => (
            <Message key={idx} role={msg.role} content={msg.content} toolCalls={msg.toolCalls} />
          ))}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
}

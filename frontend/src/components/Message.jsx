import React from "react";
import ToolBadge from "./ToolBadge";

export default function Message({ role, content, toolCalls }) {
  const isUser = role === "user";

  return (
    <div className={`py-6 px-4 md:px-8 border-b border-gray-900 ${isUser ? "bg-gray-950" : "bg-gray-900/60"}`}>
      <div className="max-w-3xl mx-auto flex gap-4">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${isUser ? "bg-blue-600 text-white" : "bg-purple-600 text-white"}`}>
          {isUser ? "U" : "S"}
        </div>
        
        <div className="flex-1 space-y-3">
          <div className="text-sm font-semibold text-gray-400 capitalize">
            {isUser ? "You" : "Summer"}
          </div>
          
          {toolCalls && toolCalls.length > 0 && (
            <div className="flex flex-wrap gap-2 py-1">
              {toolCalls.map((tc, idx) => (
                <ToolBadge key={idx} name={tc.function?.name || tc.name} />
              ))}
            </div>
          )}

          <div className="text-gray-100 leading-relaxed whitespace-pre-wrap text-sm md:text-base">
            {content || <span className="text-gray-500 italic">Thinking...</span>}
          </div>
        </div>
      </div>
    </div>
  );
}

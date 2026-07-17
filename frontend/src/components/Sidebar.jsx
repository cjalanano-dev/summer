import React from "react";

export default function Sidebar({ status, onNewChat }) {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col h-full text-gray-300">
      <div className="p-4 border-b border-gray-800 flex flex-col gap-2">
        <h2 className="text-xl font-bold text-white tracking-wide">Summer</h2>
        <div className="flex items-center gap-2 text-xs font-semibold">
          <span className={status === "connected" ? "text-green-500" : "text-red-500"}>●</span>
          <span className="text-gray-400 capitalize">{status}</span>
        </div>
      </div>

      <div className="p-4">
        <button
          onClick={onNewChat}
          className="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm font-medium transition-all duration-200 border border-gray-700 shadow-sm flex items-center justify-center gap-2"
        >
          <span>+</span> New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 py-4 space-y-2">
        <div className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Conversations
        </div>
        <div className="px-3 py-2 text-sm text-gray-400 hover:bg-gray-850 rounded-lg cursor-pointer transition">
          Default Session
        </div>
      </div>

      <div className="p-4 border-t border-gray-800 text-xs text-gray-500 text-center">
        Summer v0.6.0
      </div>
    </div>
  );
}

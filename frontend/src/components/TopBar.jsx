import React from "react";

export default function TopBar({ status }) {
  return (
    <div className="h-16 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-6 text-gray-300">
      <div className="flex items-center gap-3">
        <span className="font-semibold text-white">Default Session</span>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm bg-gray-800 px-3 py-1.5 rounded-full border border-gray-700">
          <span className={status === "connected" ? "text-green-500" : "text-red-500"}>●</span>
          <span className="text-gray-300 text-xs font-semibold capitalize">{status}</span>
        </div>
      </div>
    </div>
  );
}

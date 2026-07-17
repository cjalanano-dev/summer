import React, { useRef, useEffect } from "react";

export default function InputBox({ onSend, disabled }) {
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e?.preventDefault();
    const val = textareaRef.current?.value.strip ? textareaRef.current?.value.trim() : textareaRef.current?.value;
    if (val && !disabled) {
      onSend(val);
      if (textareaRef.current) textareaRef.current.value = "";
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="p-4 bg-gray-900 border-t border-gray-800">
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-3 relative">
        <textarea
          ref={textareaRef}
          onKeyDown={handleKeyDown}
          placeholder={disabled ? "Please wait..." : "Type your message..."}
          disabled={disabled}
          rows={1}
          className="flex-1 bg-gray-950 text-white placeholder-gray-500 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-600 border border-gray-800 resize-none max-h-36 min-h-[48px]"
        />
        <button
          type="submit"
          disabled={disabled}
          className="absolute right-3 bottom-3 p-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-55 disabled:hover:bg-blue-600 transition duration-150"
        >
          🛩️
        </button>
      </form>
    </div>
  );
}

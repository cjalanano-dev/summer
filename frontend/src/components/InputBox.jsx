import { useEffect, useRef } from "react";

export default function InputBox({ onSend, disabled, currentModel, models, modelLoading, onModelChange }) {
  const textareaRef = useRef(null);
  const activeModel = currentModel || models[0] || "qwen2.5:latest";

  useEffect(() => {
    const node = textareaRef.current;
    if (!node) return;
    node.style.height = "0px";
    node.style.height = `${Math.min(node.scrollHeight, 160)}px`;
  }, []);

  const adjustHeight = () => {
    const node = textareaRef.current;
    if (!node) return;
    node.style.height = "0px";
    node.style.height = `${Math.min(node.scrollHeight, 160)}px`;
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    const val = textareaRef.current?.value.trim();
    if (val && !disabled) {
      onSend(val);
      if (textareaRef.current) textareaRef.current.value = "";
      adjustHeight();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-white/10 bg-slate-950/70 backdrop-blur-xl px-4 pb-4 pt-3 sm:px-6 lg:px-8">
      <form onSubmit={handleSubmit} className="mx-auto w-full max-w-6xl">
        <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-3 shadow-2xl shadow-black/20">
          <div className="mb-3 flex flex-wrap items-center justify-between gap-3 px-1">
            <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-gray-300">
              <span className="uppercase tracking-[0.24em] text-gray-500">Model</span>
              <select
                value={activeModel}
                onChange={(e) => onModelChange(e.target.value)}
                disabled={modelLoading || !models.length}
                className="bg-transparent text-sm text-white outline-none disabled:opacity-50"
              >
                {(models.length ? models : [activeModel]).map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </div>

            <div className="text-xs text-gray-500">
              {modelLoading ? "Loading models..." : `${models.length || 1} available model${(models.length || 1) === 1 ? "" : "s"}`}
            </div>
          </div>

          <div className="flex items-end gap-3">
            <textarea
              ref={textareaRef}
              onChange={adjustHeight}
              onKeyDown={handleKeyDown}
              placeholder={disabled ? "Please wait..." : "Ask Summer anything..."}
              disabled={disabled}
              rows={1}
              className="min-h-[56px] flex-1 resize-none rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-4 text-[15px] leading-6 text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-sky-500/40"
            />
            <button
              type="submit"
              disabled={disabled}
              className="inline-flex h-14 w-14 items-center justify-center rounded-2xl border border-white/10 bg-white text-slate-950 transition hover:scale-[1.02] disabled:cursor-not-allowed disabled:opacity-40"
              aria-label="Send message"
            >
              ↗
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

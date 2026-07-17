import { useEffect, useRef } from "react";
import { useChatStore } from "../../store/chatStore";

export default function InputBox() {
  const sendMessage = useChatStore((s) => s.sendMessage);
  const loading = useChatStore((s) => s.loading);
  const status = useChatStore((s) => s.status);
  const currentModel = useChatStore((s) => s.currentModel);
  const models = useChatStore((s) => s.models);
  const modelLoading = useChatStore((s) => s.modelLoading);
  const setCurrentModel = useChatStore((s) => s.setCurrentModel);

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
    if (val && !loading) {
      sendMessage(val);
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
    <div className="border-t border-neutral-800 bg-neutral-950/80 backdrop-blur-xl px-4 pb-3 pt-2 sm:px-6 lg:px-8">
      <form onSubmit={handleSubmit} className="mx-auto w-full max-w-6xl">
        <div className="rounded-xl border border-neutral-800 bg-neutral-950 p-2">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2 px-2">
            <div className="flex items-center gap-2 rounded-md border border-neutral-800 bg-neutral-900 px-2.5 py-1 text-xs text-neutral-500">
              <span className="uppercase tracking-[0.15em] text-neutral-600">Model</span>
              <select
                value={activeModel}
                onChange={(e) => setCurrentModel(e.target.value)}
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
            <div className="text-xs text-neutral-600">
              {modelLoading
                ? "Loading models..."
                : `${models.length || 1} available model${(models.length || 1) === 1 ? "" : "s"}`}
            </div>
          </div>

          <div className="flex items-end gap-2">
            <textarea
              ref={textareaRef}
              onChange={adjustHeight}
              onKeyDown={handleKeyDown}
              placeholder={loading ? "Please wait..." : "Ask Summer anything..."}
              disabled={loading}
              rows={1}
              className="min-h-[48px] flex-1 resize-none rounded-lg border border-neutral-800 bg-black px-4 py-3 text-[15px] leading-6 text-white placeholder:text-neutral-600 focus:outline-none focus:ring-1 focus:ring-neutral-700"
            />
            <button
              type="submit"
              disabled={loading || status !== "connected"}
              className="inline-flex h-12 w-12 items-center justify-center rounded-lg border border-neutral-700 bg-neutral-800 text-neutral-300 transition hover:bg-neutral-700 disabled:cursor-not-allowed disabled:opacity-30"
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

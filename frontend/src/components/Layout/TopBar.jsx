import { useChatStore } from "../../store/chatStore";

export default function TopBar() {
  const status = useChatStore((s) => s.status);
  const currentModel = useChatStore((s) => s.currentModel);
  const models = useChatStore((s) => s.models);
  const modelLoading = useChatStore((s) => s.modelLoading);
  const setCurrentModel = useChatStore((s) => s.setCurrentModel);

  const activeModel = currentModel || models[0] || "qwen2.5:latest";

  return (
    <div className="sticky top-0 z-20 border-b border-neutral-800 bg-neutral-950/80 backdrop-blur-xl text-neutral-400">
      <div className="mx-auto flex h-14 w-full max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-neutral-700 bg-neutral-900 text-sm font-semibold text-white">
            S
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold text-white">Summer</div>
            <div className="text-xs text-neutral-600">Local AI workspace assistant</div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-1.5 text-xs text-neutral-400">
            <span className="uppercase tracking-[0.2em] text-neutral-600">Model</span>
            <select
              value={activeModel}
              onChange={(e) => setCurrentModel(e.target.value)}
              disabled={modelLoading || !models.length}
              className="bg-transparent text-sm text-white outline-none disabled:opacity-50"
            >
              {(models.length ? models : [activeModel]).map((model) => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2 rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-1.5 text-xs font-medium capitalize text-neutral-400">
            <span className={status === "connected" ? "text-white" : "text-neutral-700"}>●</span>
            <span>{status}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

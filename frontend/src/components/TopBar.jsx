export default function TopBar({ status, currentModel, models, modelLoading, onModelChange }) {
  const activeModel = currentModel || models[0] || "qwen2.5:latest";

  return (
    <div className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl text-gray-300">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-sm font-semibold text-white">
            S
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold text-white">Summer</div>
            <div className="text-xs text-gray-500">Local AI workspace assistant</div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-gray-300">
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

          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-medium capitalize text-gray-300">
            <span className={status === "connected" ? "text-emerald-400" : "text-rose-400"}>●</span>
            <span>{status}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

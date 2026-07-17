export default function Sidebar({ status, onNewChat }) {
  return (
    <div className="hidden w-72 flex-col border-r border-white/10 bg-slate-950/50 text-gray-300 backdrop-blur-xl lg:flex">
      <div className="border-b border-white/10 p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/5 text-sm font-semibold text-white">
            S
          </div>
          <div>
            <h2 className="text-base font-semibold tracking-tight text-white">Summer</h2>
            <p className="text-xs text-gray-500">Minimal local assistant</p>
          </div>
        </div>
      </div>

      <div className="p-4">
        <button
          onClick={onNewChat}
          className="flex w-full items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white px-4 py-3 text-sm font-medium text-slate-950 transition hover:scale-[1.01]"
        >
          <span>+</span> New chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-2">
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-3 text-xs text-gray-500">
          <div className="mb-2 uppercase tracking-[0.24em]">Status</div>
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <span className={status === "connected" ? "text-emerald-400" : "text-rose-400"}>●</span>
            <span className="capitalize">{status}</span>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10 p-4 text-center text-xs text-gray-500">
        Summer v0.6.0
      </div>
    </div>
  );
}

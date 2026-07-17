export default function ToolBadge({ name }) {
  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-900/30 text-blue-400 border border-blue-800/50 animate-pulse">
      🔧 {name}
    </span>
  );
}

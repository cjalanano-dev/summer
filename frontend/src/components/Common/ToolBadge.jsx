export default function ToolBadge({ name }) {
  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-800 text-neutral-300 border border-neutral-700 animate-pulse">
      {name}
    </span>
  );
}

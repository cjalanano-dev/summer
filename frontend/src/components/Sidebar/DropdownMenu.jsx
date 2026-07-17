import { useState, useRef, useEffect } from "react";

export default function DropdownMenu({ onRename, onPin, onArchive, onDelete, isPinned, isArchived }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    if (open) document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [open]);

  return (
    <div ref={ref} className="relative shrink-0">
      <button
        onClick={(e) => { e.stopPropagation(); setOpen(!open); }}
        className="rounded-md px-1.5 py-0.5 text-sm text-neutral-600 transition hover:text-white"
        title="More"
      >
        ⋮
      </button>
      {open && (
        <div className="absolute right-0 top-7 z-50 w-40 rounded-xl border border-neutral-700 bg-neutral-900 py-1 shadow-2xl shadow-black/60">
          <button
            onClick={(e) => { e.stopPropagation(); setOpen(false); onRename(); }}
            className="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-neutral-400 transition hover:bg-neutral-800 hover:text-white"
          >
            ✎ Rename
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); setOpen(false); onPin(!isPinned); }}
            className="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-neutral-400 transition hover:bg-neutral-800 hover:text-white"
          >
            {isPinned ? "📌 Unpin" : "📌 Pin"}
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); setOpen(false); onArchive(!isArchived); }}
            className="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-neutral-400 transition hover:bg-neutral-800 hover:text-white"
          >
            {isArchived ? "📦 Unarchive" : "📦 Archive"}
          </button>
          <div className="my-1 border-t border-neutral-800" />
          <button
            onClick={(e) => { e.stopPropagation(); setOpen(false); onDelete(); }}
            className="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-neutral-500 transition hover:bg-neutral-800 hover:text-white"
          >
            🗑 Delete
          </button>
        </div>
      )}
    </div>
  );
}

import { useState } from "react";
import { formatRelativeTime } from "../../utils/time";
import DropdownMenu from "./DropdownMenu";

export default function ConversationItem({ conversation, isActive, onSelect, onRename, onPin, onArchive, onDelete }) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(conversation.title);

  const handleRenameSubmit = () => {
    const trimmed = editTitle.trim();
    if (trimmed && trimmed !== conversation.title) {
      onRename(conversation.id, trimmed);
    } else {
      setEditTitle(conversation.title);
    }
    setEditing(false);
  };

  const startRename = () => {
    setEditTitle(conversation.title);
    setEditing(true);
  };

  if (editing) {
    return (
      <div
        className={`flex items-center gap-1 rounded-lg px-3 py-2 text-sm transition ${
          isActive ? "bg-neutral-800 text-white" : "text-neutral-400"
        }`}
      >
        <input
          autoFocus
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          onBlur={handleRenameSubmit}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleRenameSubmit();
            if (e.key === "Escape") {
              setEditTitle(conversation.title);
              setEditing(false);
            }
          }}
          className="min-w-0 flex-1 bg-transparent text-sm text-white outline-none"
        />
      </div>
    );
  }

  const titleLabel = conversation.pinned ? `📌 ${conversation.title}` : conversation.title;

  return (
    <div
      onClick={() => onSelect(conversation.id)}
      className={`group flex items-center gap-1 rounded-lg px-3 py-2 text-sm transition cursor-pointer ${
        isActive
          ? "bg-neutral-800 text-white"
          : "text-neutral-500 hover:bg-neutral-900 hover:text-neutral-300"
      }`}
    >
      <div className="min-w-0 flex-1">
        <div className="truncate">{titleLabel}</div>
        <div className="text-[11px] text-neutral-700">
          {formatRelativeTime(conversation.updated_at)}
          {conversation.archived && " • archived"}
        </div>
      </div>
      <DropdownMenu
        onRename={startRename}
        onPin={(v) => onPin(conversation.id, v)}
        onArchive={(v) => onArchive(conversation.id, v)}
        onDelete={() => onDelete(conversation.id)}
        isPinned={conversation.pinned}
        isArchived={conversation.archived}
      />
    </div>
  );
}

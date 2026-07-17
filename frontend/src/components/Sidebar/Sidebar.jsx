import { useChatStore } from "../../store/chatStore";
import ConversationItem from "./ConversationItem";

export default function Sidebar() {
  const status = useChatStore((s) => s.status);
  const conversations = useChatStore((s) => s.conversations);
  const currentConversationId = useChatStore((s) => s.currentConversationId);
  const searchQuery = useChatStore((s) => s.searchQuery);
  const selectConversation = useChatStore((s) => s.selectConversation);
  const createConversation = useChatStore((s) => s.createConversation);
  const renameConversation = useChatStore((s) => s.renameConversation);
  const confirmDeleteConversation = useChatStore((s) => s.confirmDeleteConversation);
  const pinConversation = useChatStore((s) => s.pinConversation);
  const archiveConversation = useChatStore((s) => s.archiveConversation);
  const searchConversations = useChatStore((s) => s.searchConversations);

  const pinned = conversations?.filter((c) => c.pinned) || [];
  const unpinned = conversations?.filter((c) => !c.pinned) || [];

  return (
    <div className="hidden w-72 flex-col border-r border-neutral-800 bg-neutral-950 text-neutral-400 lg:flex">
      <div className="border-b border-neutral-800 px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-neutral-700 bg-neutral-900 text-sm font-semibold text-white">
            S
          </div>
          <div>
            <h2 className="text-sm font-semibold tracking-tight text-white">Summer</h2>
            <p className="text-xs text-neutral-600">Minimal local assistant</p>
          </div>
        </div>
      </div>

      <div className="px-4 py-3">
        <div className="relative mb-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => searchConversations(e.target.value)}
            placeholder="Search..."
            className="w-full rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-white placeholder:text-neutral-600 outline-none transition focus:border-neutral-700"
          />
        </div>
        <button
          onClick={createConversation}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-neutral-700 bg-neutral-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-neutral-800"
        >
          <span className="text-neutral-500">+</span> New chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-3 py-1">
        {conversations && conversations.length > 0 ? (
          <div className="space-y-0.5">
            {pinned.map((conv) => (
              <ConversationItem
                key={conv.id}
                conversation={conv}
                isActive={conv.id === currentConversationId}
                onSelect={selectConversation}
                onRename={renameConversation}
                onPin={pinConversation}
                onArchive={archiveConversation}
                onDelete={confirmDeleteConversation}
              />
            ))}
            {pinned.length > 0 && unpinned.length > 0 && (
              <div className="my-2 border-t border-neutral-800" />
            )}
            {unpinned.map((conv) => (
              <ConversationItem
                key={conv.id}
                conversation={conv}
                isActive={conv.id === currentConversationId}
                onSelect={selectConversation}
                onRename={renameConversation}
                onPin={pinConversation}
                onArchive={archiveConversation}
                onDelete={confirmDeleteConversation}
              />
            ))}
          </div>
        ) : (
          <div className="rounded-lg border border-neutral-800 bg-neutral-900 p-4 text-center text-xs text-neutral-600">
            {searchQuery ? "No matching conversations" : "No conversations yet"}
          </div>
        )}
      </div>

      <div className="border-t border-neutral-800 px-4 py-3">
        <div className="flex items-center gap-2 text-xs text-neutral-600">
          <span className={status === "connected" ? "text-white" : "text-neutral-700"}>●</span>
          <span className="capitalize">{status}</span>
        </div>
        <div className="mt-1 text-xs text-neutral-700">Summer v0.7.0</div>
      </div>
    </div>
  );
}

import { useChatStore } from "../../store/chatStore";

export default function ConfirmModal() {
  const confirmDeleteId = useChatStore((s) => s.confirmDeleteId);
  const cancelDelete = useChatStore((s) => s.cancelDelete);
  const deleteConversation = useChatStore((s) => s.deleteConversation);

  if (!confirmDeleteId) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-sm rounded-xl border border-neutral-700 bg-neutral-950 p-6 shadow-2xl shadow-black/60">
        <h3 className="text-base font-semibold text-white">Delete Conversation?</h3>
        <p className="mt-2 text-sm text-neutral-500">This cannot be undone.</p>
        <div className="mt-5 flex justify-end gap-3">
          <button
            onClick={cancelDelete}
            className="rounded-lg border border-neutral-700 bg-neutral-900 px-4 py-2 text-sm font-medium text-neutral-400 transition hover:bg-neutral-800"
          >
            Cancel
          </button>
          <button
            onClick={() => deleteConversation(confirmDeleteId)}
            className="rounded-lg bg-neutral-700 px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-600"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

import { create } from "zustand";
import * as api from "../services/api";

function mergeStreamChunk(existing, chunk) {
  if (!chunk) return existing;
  if (!existing) return chunk;
  if (chunk.startsWith(existing)) return existing + chunk.slice(existing.length);
  if (existing.startsWith(chunk)) return existing;
  return existing + chunk;
}

export const useChatStore = create((set, get) => ({
  status: "checking",
  models: [],
  currentModel: "",
  modelLoading: true,
  conversations: [],
  currentConversationId: null,
  messages: [],
  searchQuery: "",
  confirmDeleteId: null,
  loading: false,

  bootstrap: async () => {
    try {
      const [healthRes, modelData] = await Promise.all([
        api.fetchHealth(),
        api.fetchModels(),
      ]);

      const availableModels = modelData.models || [];
      const nextModel = modelData.currentModel || availableModels[0] || "";

      set({
        models: availableModels,
        currentModel: nextModel,
        status: "connected",
      });

      const convList = await api.listConversations();
      if (convList && convList.length > 0) {
        set({ currentConversationId: convList[0].id });
        const msgs = await api.getMessages(convList[0].id);
        set({
          conversations: convList,
          messages: msgs.map((m) => ({ role: m.role, content: m.content })),
        });
      } else {
        await get().createConversation();
      }
    } catch {
      set({ status: "error" });
    } finally {
      set({ modelLoading: false });
    }
  },

  setCurrentModel: async (model) => {
    set({ currentModel: model });
    try {
      await api.selectModel(model);
    } catch {
      // ignore
    }
  },

  createConversation: async () => {
    try {
      const conv = await api.createConversation("New Chat");
      set((s) => ({
        conversations: [conv, ...s.conversations],
        currentConversationId: conv.id,
        messages: [],
        searchQuery: "",
      }));
      return conv;
    } catch {
      // ignore
    }
  },

  selectConversation: async (id) => {
    set({ currentConversationId: id, messages: [], searchQuery: "" });
    try {
      const msgs = await api.getMessages(id);
      set({ messages: msgs.map((m) => ({ role: m.role, content: m.content })) });
    } catch {
      set({ messages: [] });
    }
  },

  sendMessage: async (text) => {
    const { currentConversationId, currentModel, messages } = get();
    if (!currentConversationId) return;

    const updatedMessages = [...messages, { role: "user", content: text }];
    set({ messages: updatedMessages, loading: true });

    try {
      const response = await api.sendMessage(currentConversationId, text, currentModel);

      if (!response.body) throw new Error("No response stream");

      set((s) => ({
        messages: [...s.messages, { role: "assistant", content: "" }],
      }));

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const cleanLine = line.trim();
          if (cleanLine.startsWith("data: ")) {
            try {
              const payload = JSON.parse(cleanLine.substring(6));
              if (payload.content) {
                set((s) => {
                  const copy = [...s.messages];
                  const lastIndex = copy.length - 1;
                  const last = copy[lastIndex];
                  if (last && last.role === "assistant") {
                    copy[lastIndex] = {
                      ...last,
                      content: mergeStreamChunk(last.content, payload.content),
                    };
                  }
                  return { messages: copy };
                });
              } else if (payload.error) {
                console.error("SSE Error:", payload.error);
              }
            } catch {
              // ignore split JSON
            }
          }
        }
      }

      // Refresh conversation list to pick up auto-generated title
      get().fetchConversationList();
    } catch (err) {
      console.error(err);
      set((s) => ({
        messages: [
          ...s.messages,
          { role: "assistant", content: "Error: Failed to fetch response from Summer." },
        ],
      }));
    } finally {
      set({ loading: false });
    }
  },

  fetchConversationList: async () => {
    try {
      const data = await api.listConversations();
      set({ conversations: data });
    } catch {
      // ignore
    }
  },

  renameConversation: async (id, title) => {
    try {
      const updated = await api.updateConversation(id, { title });
      set((s) => ({
        conversations: s.conversations.map((c) =>
          c.id === id ? { ...c, title: updated.title } : c
        ),
      }));
    } catch {
      // ignore
    }
  },

  deleteConversation: async (id) => {
    set({ confirmDeleteId: null });

    try {
      await api.deleteConversation(id);
      const { conversations, currentConversationId } = get();
      const remaining = conversations.filter((c) => c.id !== id);
      set({ conversations: remaining });

      if (currentConversationId === id) {
        if (remaining.length > 0) {
          const next = remaining[0];
          set({ currentConversationId: next.id, messages: [] });
          const msgs = await api.getMessages(next.id);
          set({ messages: msgs.map((m) => ({ role: m.role, content: m.content })) });
        } else {
          set({ currentConversationId: null, messages: [] });
          await get().createConversation();
        }
      }
    } catch {
      // ignore
    }
  },

  confirmDeleteConversation: (id) => {
    set({ confirmDeleteId: id });
  },

  cancelDelete: () => {
    set({ confirmDeleteId: null });
  },

  pinConversation: async (id, pinned) => {
    try {
      const updated = await api.updateConversation(id, { pinned });
      set((s) => {
        const next = s.conversations.map((c) =>
          c.id === id ? { ...c, pinned: updated.pinned } : c
        );
        next.sort(
          (a, b) =>
            (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0) ||
            new Date(b.updated_at) - new Date(a.updated_at)
        );
        return { conversations: next };
      });
    } catch {
      // ignore
    }
  },

  archiveConversation: async (id, archived) => {
    try {
      const updated = await api.updateConversation(id, { archived });
      set((s) => ({
        conversations: s.conversations.map((c) =>
          c.id === id ? { ...c, archived: updated.archived } : c
        ),
      }));
    } catch {
      // ignore
    }
  },

  searchConversations: async (query) => {
    set({ searchQuery: query });
    if (!query.trim()) {
      try {
        const data = await api.listConversations();
        set({ conversations: data });
      } catch {
        // ignore
      }
      return;
    }
    try {
      const data = await api.searchConversations(query);
      set({ conversations: data });
    } catch {
      // ignore
    }
  },
}));

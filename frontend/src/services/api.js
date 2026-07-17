const BASE = "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed: ${res.status}`);
  }
  return res;
}

export function fetchHealth() {
  return request("/health");
}

export async function fetchModels() {
  const res = await request("/models");
  return res.json();
}

export async function selectModel(model) {
  const res = await request("/models/select", {
    method: "POST",
    body: JSON.stringify({ model }),
  });
  return res.json();
}

export async function listConversations() {
  const res = await request("/conversations");
  return res.json();
}

export async function createConversation(title = "New Chat") {
  const res = await request("/conversations", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
  return res.json();
}

export async function getConversation(id) {
  const res = await request(`/conversations/${id}`);
  return res.json();
}

export async function updateConversation(id, fields) {
  const res = await request(`/conversations/${id}`, {
    method: "PATCH",
    body: JSON.stringify(fields),
  });
  return res.json();
}

export async function deleteConversation(id) {
  await request(`/conversations/${id}`, { method: "DELETE" });
}

export async function searchConversations(query) {
  const res = await request(`/conversations/search/${encodeURIComponent(query)}`);
  return res.json();
}

export async function getMessages(id) {
  const res = await request(`/conversations/${id}/messages`);
  return res.json();
}

export async function addMessage(id, role, content, metadata) {
  const res = await request(`/conversations/${id}/messages`, {
    method: "POST",
    body: JSON.stringify({ role, content, metadata }),
  });
  return res.json();
}

export async function sendMessage(conversationId, message, model) {
  return request("/chat", {
    method: "POST",
    body: JSON.stringify({
      conversation_id: conversationId,
      message,
      model: model || undefined,
    }),
  });
}

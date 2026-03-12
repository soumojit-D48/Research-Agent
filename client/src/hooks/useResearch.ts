import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getUserId } from "@/lib/userId";

// ── Health ─────────────────────────────────────────────────────────────────
export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: () => api.health(),
    staleTime: 30_000,
  });
}

// ── Run research ───────────────────────────────────────────────────────────
export function useRunResearch() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (query: string) => api.research.run(query, getUserId()),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
}

// ── Conversations ──────────────────────────────────────────────────────────
export function useConversations() {
  return useQuery({
    queryKey: ["conversations", getUserId()],
    queryFn: () => api.conversations.getByUser(getUserId()),
    staleTime: 10_000,
  });
}

export function useConversation(id: string) {
  return useQuery({
    queryKey: ["conversation", id],
    queryFn: () => api.conversations.getById(id),
    enabled: !!id,
  });
}

export function useDeleteConversation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.conversations.delete(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
}

// ── Agent logs ─────────────────────────────────────────────────────────────
export function useAgentLogs(conversationId: string) {
  return useQuery({
    queryKey: ["logs", conversationId],
    queryFn: () => api.logs.getByConversation(conversationId),
    enabled: !!conversationId,
  });
}

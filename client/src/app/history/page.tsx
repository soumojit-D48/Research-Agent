"use client";

import { Clock, RefreshCw } from "lucide-react";
import { useConversations, useDeleteConversation } from "@/hooks/useResearch";
import ConversationList from "@/components/research/ConversationList";
import { useState } from "react";

export default function History() {
  const { data: conversations = [], isLoading, refetch } = useConversations();
  const { mutate: del } = useDeleteConversation();
  const [deleting, setDeleting] = useState<string | null>(null);

  const handleDelete = (id: string) => {
    setDeleting(id);
    del(id, { onSettled: () => setDeleting(null) });
  };

  return (
    <div className="flex-1 px-6 py-8 max-w-3xl mx-auto w-full space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: "var(--color-card)", border: "1px solid var(--color-border)" }}
          >
            <Clock size={18} style={{ color: "var(--color-primary)" }} />
          </div>
          <div>
            <h1 className="text-xl font-semibold" style={{ color: "var(--color-foreground)" }}>
              Research History
            </h1>
            <p className="text-xs" style={{ color: "var(--color-muted-foreground)" }}>
              {conversations.length} conversation{conversations.length !== 1 ? "s" : ""}
            </p>
          </div>
        </div>
        <button
          onClick={() => refetch()}
          className="p-2 rounded-lg transition-colors"
          style={{ color: "var(--color-muted-foreground)", backgroundColor: "var(--color-card)", border: "1px solid var(--color-border)" }}
          title="Refresh"
        >
          <RefreshCw size={15} />
        </button>
      </div>

      {/* List */}
      {isLoading ? (
        <div className="space-y-3">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="rounded-xl border p-4 flex gap-4"
              style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
            >
              <div className="w-10 h-10 rounded-xl shimmer flex-shrink-0" />
              <div className="flex-1 space-y-2">
                <div className="h-4 rounded shimmer w-3/4" />
                <div className="h-3 rounded shimmer w-1/3" />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <ConversationList
          conversations={conversations}
          onDelete={handleDelete}
          deleting={deleting}
        />
      )}
    </div>
  );
}

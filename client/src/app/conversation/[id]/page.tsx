"use client";

import { ArrowLeft, MessageSquare, Bot, Terminal } from "lucide-react";
import { useConversation, useAgentLogs } from "@/hooks/useResearch";
import MessageBubble from "@/components/research/MessageBubble";
import AgentLogViewer from "@/components/research/AgentLogViewer";
import { useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

function fmtDate(iso: string) {
  return new Date(iso).toLocaleString("en-US", {
    month: "short", day: "numeric", year: "numeric",
    hour: "numeric", minute: "2-digit",
  });
}

export default function ConversationDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: conv, isLoading } = useConversation(id ?? "");
  const { data: logs = [] } = useAgentLogs(id ?? "");
  const [showLogs, setShowLogs] = useState(false);

  if (!id) return null;

  return (
    <div className="flex-1 px-6 py-8 max-w-3xl mx-auto w-full space-y-6 animate-fade-in">
      {/* Back */}
      <Link
        href="/history"
        className="inline-flex items-center gap-2 text-sm transition-colors"
        style={{ color: "var(--color-muted-foreground)" }}
        onMouseEnter={(e) => (e.currentTarget.style.color = "var(--color-primary)")}
        onMouseLeave={(e) => (e.currentTarget.style.color = "var(--color-muted-foreground)")}
      >
        <ArrowLeft size={15} /> Back to history
      </Link>

      {/* Meta */}
      {conv && (
        <div
          className="rounded-xl border px-5 py-4 flex items-center justify-between"
          style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
        >
          <div className="flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center"
              style={{ backgroundColor: "color-mix(in srgb, var(--color-primary) 12%, transparent)" }}
            >
              <MessageSquare size={16} style={{ color: "var(--color-primary)" }} />
            </div>
            <div>
              <p className="text-sm font-medium" style={{ color: "var(--color-foreground)" }}>
                Conversation
              </p>
              <p className="text-xs font-mono" style={{ color: "var(--color-muted-foreground)" }}>
                {conv.id.slice(0, 8)}…
              </p>
            </div>
          </div>
          <p className="text-xs" style={{ color: "var(--color-muted-foreground)" }}>
            {fmtDate(conv.created_at)}
          </p>
        </div>
      )}

      {/* Messages */}
      <div
        className="rounded-2xl border overflow-hidden"
        style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
      >
        <div
          className="px-5 py-4 border-b flex items-center gap-2"
          style={{ borderColor: "var(--color-border)" }}
        >
          <Bot size={15} style={{ color: "var(--color-primary)" }} />
          <span className="text-sm font-medium" style={{ color: "var(--color-foreground)" }}>
            Messages
          </span>
        </div>

        <div className="px-5 py-5 space-y-4">
          {isLoading ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className={`flex gap-3 ${i % 2 === 0 ? "justify-start" : "justify-end"}`}>
                  <div className="w-8 h-8 rounded-full shimmer" />
                  <div className="h-14 rounded-2xl shimmer w-64" />
                </div>
              ))}
            </div>
          ) : conv?.messages.length ? (
            conv.messages.map((m, i) => <MessageBubble key={i} message={m} />)
          ) : (
            <p className="text-sm text-center py-4" style={{ color: "var(--color-muted-foreground)" }}>
              No messages in this conversation.
            </p>
          )}
        </div>
      </div>

      {/* Agent logs toggle */}
      {logs.length > 0 && (
        <div
          className="rounded-2xl border overflow-hidden"
          style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
        >
          <button
            onClick={() => setShowLogs((v) => !v)}
            className="w-full px-5 py-4 flex items-center gap-2 text-left border-b"
            style={{ borderColor: "var(--color-border)" }}
          >
            <Terminal size={15} style={{ color: "var(--color-primary)" }} />
            <span className="text-sm font-medium flex-1" style={{ color: "var(--color-foreground)" }}>
              Agent Execution Logs
            </span>
            <span className="text-xs px-2 py-0.5 rounded-full" style={{ backgroundColor: "var(--color-muted)", color: "var(--color-muted-foreground)" }}>
              {logs.length}
            </span>
            <span className="text-xs" style={{ color: "var(--color-muted-foreground)" }}>{showLogs ? "▲ hide" : "▼ show"}</span>
          </button>
          {showLogs && (
            <div className="px-5 py-5">
              <AgentLogViewer logs={logs} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

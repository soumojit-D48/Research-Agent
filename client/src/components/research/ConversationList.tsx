import Link from "next/link";
import { MessageSquare, Trash2, ChevronRight, Calendar, Hash } from "lucide-react";
import type { Conversation } from "@/lib/api";

interface ConversationListProps {
  conversations: Conversation[];
  onDelete?: (id: string) => void;
  deleting?: string | null;
}

function fmtDate(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function preview(conv: Conversation) {
  const first = conv.messages.find((m) => m.role === "user");
  return first?.content ?? "No messages";
}

export default function ConversationList({ conversations, onDelete, deleting }: ConversationListProps) {
  if (!conversations.length)
    return (
      <div className="text-center py-16 space-y-3">
        <MessageSquare size={40} className="mx-auto opacity-30" style={{ color: "var(--color-muted-foreground)" }} />
        <p className="text-sm" style={{ color: "var(--color-muted-foreground)" }}>No research conversations yet.</p>
        <Link
          href="/"
          className="inline-block text-sm px-4 py-2 rounded-xl font-medium"
          style={{ backgroundColor: "var(--color-primary)", color: "var(--color-primary-foreground)" }}
        >
          Start researching
        </Link>
      </div>
    );

  return (
    <div className="space-y-3">
      {conversations.map((c) => (
        <div
          key={c.id}
          className="group relative rounded-xl border transition-all duration-200"
          style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLDivElement).style.borderColor = "var(--color-primary)";
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLDivElement).style.borderColor = "var(--color-border)";
          }}
        >
          <Link href={`/conversation/${c.id}`} className="flex items-start gap-4 p-4 pr-12">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
              style={{ backgroundColor: "var(--color-muted)" }}
            >
              <MessageSquare size={18} style={{ color: "var(--color-primary)" }} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate mb-1" style={{ color: "var(--color-foreground)" }}>
                {preview(c)}
              </p>
              <div className="flex items-center gap-3 text-xs" style={{ color: "var(--color-muted-foreground)" }}>
                <span className="flex items-center gap-1">
                  <Calendar size={11} /> {fmtDate(c.created_at)}
                </span>
                <span className="flex items-center gap-1">
                  <Hash size={11} /> {c.messages.length} msg
                </span>
              </div>
            </div>
            <ChevronRight size={16} className="self-center opacity-40" />
          </Link>

          {onDelete && (
            <button
              onClick={(e) => { e.preventDefault(); onDelete(c.id); }}
              disabled={deleting === c.id}
              className="absolute top-4 right-10 opacity-0 group-hover:opacity-100 p-1.5 rounded-lg transition-all duration-200"
              style={{ color: "var(--color-muted-foreground)" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "var(--color-destructive)")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "var(--color-muted-foreground)")}
              title="Delete"
            >
              <Trash2 size={14} />
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

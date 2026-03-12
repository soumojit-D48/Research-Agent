import { CheckCircle2, XCircle, ChevronDown, ChevronUp, Clock, Zap } from "lucide-react";
import { useState } from "react";
import type { AgentLog } from "@/lib/api";

const ACTION_LABELS: Record<string, { label: string; emoji: string }> = {
  initialize:        { label: "Initialize Agent",    emoji: "🚀" },
  generate_queries:  { label: "Generate Queries",   emoji: "🧠" },
  web_search:        { label: "Web Search",          emoji: "🔍" },
  extract_content:   { label: "Extract Content",     emoji: "📄" },
  synthesize_report: { label: "Synthesize Report",  emoji: "✍️" },
};

interface AgentLogViewerProps {
  logs: AgentLog[];
}

export default function AgentLogViewer({ logs }: AgentLogViewerProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  if (!logs.length) return (
    <p className="text-sm text-center py-8" style={{ color: "var(--color-muted-foreground)" }}>
      No agent logs available.
    </p>
  );

  const total = logs.reduce((s, l) => s + (l.execution_time ?? 0), 0);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium" style={{ color: "var(--color-muted-foreground)" }}>
          {logs.length} agent steps
        </span>
        <span className="text-xs flex items-center gap-1" style={{ color: "var(--color-muted-foreground)" }}>
          <Clock size={11} /> {(total / 1000).toFixed(1)}s total
        </span>
      </div>

      {logs.map((log) => {
        const meta = ACTION_LABELS[log.action] ?? { label: log.action, emoji: "⚙️" };
        const isOpen = expanded === log.id;
        const success = log.status === "success";

        return (
          <div
            key={log.id}
            className="rounded-xl border overflow-hidden transition-all duration-200"
            style={{
              backgroundColor: "var(--color-surface)",
              borderColor: isOpen ? "var(--color-primary)" : "var(--color-border)",
            }}
          >
            <button
              className="w-full flex items-center gap-3 px-4 py-3 text-left"
              onClick={() => setExpanded(isOpen ? null : log.id)}
            >
              <span className="text-base">{meta.emoji}</span>
              <span className="flex-1 text-sm font-medium" style={{ color: "var(--color-foreground)" }}>
                {meta.label}
              </span>
              <span className="flex items-center gap-1 text-xs" style={{ color: "var(--color-muted-foreground)" }}>
                <Zap size={11} />
                {log.execution_time ? `${log.execution_time}ms` : "—"}
              </span>
              {success
                ? <CheckCircle2 size={14} style={{ color: "hsl(142 70% 50%)" }} />
                : <XCircle size={14} style={{ color: "var(--color-destructive)" }} />
              }
              {isOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>

            {isOpen && (
              <div className="px-4 pb-4 space-y-3 border-t" style={{ borderColor: "var(--color-border)" }}>
                {Object.keys(log.input_data).length > 0 && (
                  <div>
                    <p className="text-xs font-semibold mb-1 mt-3" style={{ color: "var(--color-muted-foreground)" }}>INPUT</p>
                    <pre
                      className="text-xs rounded-lg p-3 overflow-auto"
                      style={{ backgroundColor: "var(--color-muted)", color: "var(--color-foreground)", maxHeight: "160px" }}
                    >
                      {JSON.stringify(log.input_data, null, 2)}
                    </pre>
                  </div>
                )}
                {Object.keys(log.output_data).length > 0 && (
                  <div>
                    <p className="text-xs font-semibold mb-1" style={{ color: "var(--color-muted-foreground)" }}>OUTPUT</p>
                    <pre
                      className="text-xs rounded-lg p-3 overflow-auto"
                      style={{ backgroundColor: "var(--color-muted)", color: "var(--color-foreground)", maxHeight: "160px" }}
                    >
                      {JSON.stringify(log.output_data, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

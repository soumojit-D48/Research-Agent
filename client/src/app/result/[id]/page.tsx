"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, BookOpen, Globe, Search, Copy, Check } from "lucide-react";
import { useConversation, useAgentLogs } from "@/hooks/useResearch";
import AgentLogViewer from "@/components/research/AgentLogViewer";
import type { ResearchResponse } from "@/lib/api";
import { useState } from "react";


export default function ResearchResult() {
    const params = useParams();
    const id = params?.id as string;

  const { data: conv, isLoading } = useConversation(id ?? "");
  const { data: logs = [] } = useAgentLogs(id ?? "");

  const [copied, setCopied] = useState(false);
  const [tab, setTab] = useState<"report" | "logs">("report");

  const report =
    conv?.messages.find((m) => m.role === "assistant")?.content ?? "";

  const query =
    (typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("query") : null) ??
    conv?.messages.find((m) => m.role === "user")?.content ?? "";

  const count = logs.length;

  const copyReport = () => {
    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!id) return <div className="p-8 text-center" style={{ color: "var(--color-muted-foreground)" }}>Invalid result.</div>;

  return (
    <div className="flex-1 px-6 py-8 max-w-4xl mx-auto w-full space-y-6 animate-fade-in">
      {/* Back */}
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-sm transition-colors"
        style={{ color: "var(--color-muted-foreground)" }}
        onMouseEnter={(e) => (e.currentTarget.style.color = "var(--color-primary)")}
        onMouseLeave={(e) => (e.currentTarget.style.color = "var(--color-muted-foreground)")}
      >
        <ArrowLeft size={15} /> New research
      </Link>

      {/* Query header */}
      <div
        className="rounded-2xl border p-6 space-y-3"
        style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
      >
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs" style={{ color: "var(--color-primary)" }}>
              <Search size={12} /> Research Query
            </div>
            <h1 className="text-xl font-semibold" style={{ color: "var(--color-foreground)" }}>{query}</h1>
          </div>
          {count !== undefined && (
            <div
              className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full shrink-0"
              style={{ backgroundColor: "var(--color-muted)", color: "var(--color-muted-foreground)" }}
            >
              <Globe size={11} /> {count} sources
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 p-1 rounded-xl w-fit" style={{ backgroundColor: "var(--color-muted)" }}>
        {(["report", "logs"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className="px-4 py-2 rounded-lg text-sm font-medium capitalize transition-all duration-200"
            style={{
              backgroundColor: tab === t ? "var(--color-card)" : "transparent",
              color: tab === t ? "var(--color-foreground)" : "var(--color-muted-foreground)",
              boxShadow: tab === t ? "var(--shadow-card)" : "none",
            }}
          >
            {t === "report" ? <span className="flex items-center gap-1.5"><BookOpen size={13} /> Report</span>
              : <span className="flex items-center gap-1.5">⚙️ Agent Logs {logs.length > 0 && `(${logs.length})`}</span>
            }
          </button>
        ))}
      </div>

      {/* Report tab */}
      {tab === "report" && (
        <div
          className="rounded-2xl border overflow-hidden"
          style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
        >
          <div className="flex items-center justify-between px-6 py-4 border-b" style={{ borderColor: "var(--color-border)" }}>
            <span className="text-sm font-medium" style={{ color: "var(--color-foreground)" }}>
              Research Report
            </span>
            <button
              onClick={copyReport}
              className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg transition-all duration-200"
              style={{ backgroundColor: "var(--color-muted)", color: "var(--color-muted-foreground)" }}
            >
              {copied ? <><Check size={12} /> Copied</> : <><Copy size={12} /> Copy</>}
            </button>
          </div>
          <div className="px-6 py-6">
            {isLoading && !report ? (
              <div className="space-y-3">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-4 rounded shimmer" style={{ width: `${70 + Math.random() * 30}%` }} />
                ))}
              </div>
            ) : (
              <div
                className="text-sm leading-relaxed whitespace-pre-wrap"
                style={{ color: "var(--color-foreground)" }}
              >
                {report || "Report not available."}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Logs tab */}
      {tab === "logs" && (
        <div
          className="rounded-2xl border p-6"
          style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
        >
          <AgentLogViewer logs={logs} />
        </div>
      )}
    </div>
  );
}

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Brain, Globe, FileText, Sparkles, CheckCircle2, Loader2 } from "lucide-react";
import { useRunResearch } from "@/hooks/useResearch";
import SearchBar from "@/components/research/SearchBar";

const STEPS = [
  { icon: Brain,       label: "Generating search queries…" },
  { icon: Globe,       label: "Searching the web…" },
  { icon: FileText,    label: "Extracting content…" },
  { icon: Sparkles,    label: "Synthesizing report…" },
];

export default function Index() {
  const router = useRouter();
  const { mutate, isPending } = useRunResearch();
  const [step, setStep] = useState(-1);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = (query: string) => {
    setError(null);
    setStep(0);

    // Animate through steps while waiting
    const interval = setInterval(() => {
      setStep((s) => (s < STEPS.length - 1 ? s + 1 : s));
    }, 5000);

    mutate(query, {
      onSuccess: (data) => {
        clearInterval(interval);
        setStep(-1);
        // navigate(`/result/${data.conversation_id}`, { state: { result: data, query } });
        router.push(`/result/${data.conversation_id}?query=${query}`);
      },
      onError: (err) => {
        clearInterval(interval);
        setStep(-1);
        setError(err instanceof Error ? err.message : "Research failed. Is the backend running?");
      },
    });
  };

  return (
    <div className="flex flex-col flex-1">
      {/* Hero */}
      <section className="relative flex flex-col items-center justify-center px-6 py-24 overflow-hidden">
        {/* BG image */}
        <div className="absolute inset-0 z-0">
          {/* <img src={heroBg} alt="" className="w-full h-full object-cover opacity-20" /> */}
          <div
            className="absolute inset-0"
            style={{
              background: "linear-gradient(to bottom, transparent 40%, var(--color-background) 100%)",
            }}
          />
        </div>

        <div className="relative z-10 text-center space-y-6 max-w-3xl">
          {/* Badge */}
          <div
            className="inline-flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-full border"
            style={{
              backgroundColor: "color-mix(in srgb, var(--color-primary) 10%, transparent)",
              borderColor: "color-mix(in srgb, var(--color-primary) 30%, transparent)",
              color: "var(--color-primary)",
            }}
          >
            <Sparkles size={12} />
            Powered by LangGraph + OpenRouter AI
          </div>

          <h1
            className="text-5xl font-bold tracking-tight leading-tight"
            style={{ color: "var(--color-foreground)" }}
          >
            Research anything with{" "}
            <span
              className="text-glow"
              style={{ color: "var(--color-primary)" }}
            >
              AI
            </span>
          </h1>

          <p className="text-lg" style={{ color: "var(--color-muted-foreground)" }}>
            Autonomous web research — submit a question and receive a comprehensive, cited report.
          </p>

          <SearchBar onSubmit={handleSearch} loading={isPending} />
        </div>
      </section>

      {/* Loading overlay */}
      {isPending && (
        <div className="fixed inset-0 z-50 flex items-center justify-center"
          style={{ backgroundColor: "color-mix(in srgb, var(--color-background) 85%, transparent)", backdropFilter: "blur(8px)" }}
        >
          <div
            className="rounded-2xl border p-8 space-y-6 w-full max-w-md mx-6 animate-slide-up"
            style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
          >
            <div className="flex items-center gap-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center"
                style={{ backgroundColor: "var(--color-primary)" }}
              >
                <Loader2 size={20} className="animate-spin" style={{ color: "var(--color-primary-foreground)" }} />
              </div>
              <div>
                <p className="font-semibold text-sm" style={{ color: "var(--color-foreground)" }}>AI is researching…</p>
                <p className="text-xs" style={{ color: "var(--color-muted-foreground)" }}>This may take 10–30 seconds</p>
              </div>
            </div>

            <div className="space-y-3">
              {STEPS.map((s, i) => {
                const done = i < step;
                const active = i === step;
                const Icon = s.icon;
                return (
                  <div key={i} className="flex items-center gap-3">
                    <div
                      className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 transition-all duration-500"
                      style={{
                        backgroundColor: done
                          ? "color-mix(in srgb, hsl(142 70% 50%) 15%, transparent)"
                          : active
                          ? "color-mix(in srgb, var(--color-primary) 15%, transparent)"
                          : "var(--color-muted)",
                      }}
                    >
                      {done
                        ? <CheckCircle2 size={14} style={{ color: "hsl(142 70% 50%)" }} />
                        : active
                        ? <Icon size={14} style={{ color: "var(--color-primary)" }} className="animate-pulse" />
                        : <Icon size={14} style={{ color: "var(--color-muted-foreground)", opacity: 0.4 }} />
                      }
                    </div>
                    <span
                      className="text-sm transition-all duration-300"
                      style={{
                        color: done
                          ? "hsl(142 70% 50%)"
                          : active
                          ? "var(--color-foreground)"
                          : "var(--color-muted-foreground)",
                        opacity: active || done ? 1 : 0.4,
                      }}
                    >
                      {s.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="max-w-2xl mx-auto px-6 w-full mb-8">
          <div
            className="rounded-xl border px-4 py-3 text-sm flex items-start gap-3"
            style={{ backgroundColor: "color-mix(in srgb, var(--color-destructive) 10%, transparent)", borderColor: "var(--color-destructive)", color: "var(--color-foreground)" }}
          >
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Features row */}
      <section className="px-6 pb-16 max-w-4xl mx-auto w-full">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { icon: Brain,    title: "AI Query Generation",  desc: "Generates 3–5 targeted search queries from your question" },
            { icon: Globe,    title: "Real-time Web Search", desc: "Searches DuckDuckGo and extracts relevant content live" },
            { icon: FileText, title: "Synthesized Reports",  desc: "Produces a comprehensive, structured research report" },
          ].map(({ icon: Icon, title, desc }) => (
            <div
              key={title}
              className="rounded-xl border p-5 space-y-3"
              style={{ backgroundColor: "var(--color-card)", borderColor: "var(--color-border)" }}
            >
              <div
                className="w-9 h-9 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: "color-mix(in srgb, var(--color-primary) 12%, transparent)" }}
              >
                <Icon size={18} style={{ color: "var(--color-primary)" }} />
              </div>
              <p className="text-sm font-semibold" style={{ color: "var(--color-foreground)" }}>{title}</p>
              <p className="text-xs leading-relaxed" style={{ color: "var(--color-muted-foreground)" }}>{desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

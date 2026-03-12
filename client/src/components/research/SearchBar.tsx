import { useState, useRef, useEffect } from "react";
import { Search, ArrowRight, Loader2 } from "lucide-react";

interface SearchBarProps {
  onSubmit: (query: string) => void;
  loading?: boolean;
  placeholder?: string;
}

const SUGGESTIONS = [
  "What is quantum computing?",
  "How does CRISPR gene editing work?",
  "Explain large language models",
  "What are the latest advances in fusion energy?",
  "How does blockchain consensus work?",
];

export default function SearchBar({ onSubmit, loading, placeholder }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const submit = () => {
    const q = query.trim();
    if (!q || loading) return;
    onSubmit(q);
  };

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") submit();
  };

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto space-y-4">
      {/* Input */}
      <div
        className="relative flex items-center rounded-2xl transition-all duration-300"
        style={{
          backgroundColor: "var(--color-card)",
          border: `1.5px solid ${focused ? "var(--color-primary)" : "var(--color-border)"}`,
          boxShadow: focused ? "var(--shadow-glow)" : "none",
        }}
      >
        <Search
          size={18}
          className="absolute left-4"
          style={{ color: focused ? "var(--color-primary)" : "var(--color-muted-foreground)" }}
        />
        <input
          ref={inputRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={onKey}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder={placeholder ?? "Ask anything — e.g. What is machine learning?"}
          disabled={loading}
          className="flex-1 bg-transparent outline-none py-4 pl-12 pr-4 text-sm"
          style={{ color: "var(--color-foreground)" }}
        />
        <button
          onClick={submit}
          disabled={!query.trim() || loading}
          className="mr-2 flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-40"
          style={{
            backgroundColor: "var(--color-primary)",
            color: "var(--color-primary-foreground)",
          }}
        >
          {loading ? (
            <Loader2 size={15} className="animate-spin" />
          ) : (
            <>Research <ArrowRight size={14} /></>
          )}
        </button>
      </div>

      {/* Quick suggestions */}
      <div className="flex flex-wrap gap-2 justify-center">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => { setQuery(s); inputRef.current?.focus(); }}
            className="text-xs px-3 py-1.5 rounded-full border transition-all duration-200"
            style={{
              color: "var(--color-muted-foreground)",
              borderColor: "var(--color-border)",
              backgroundColor: "var(--color-muted)",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLButtonElement).style.borderColor = "var(--color-primary)";
              (e.currentTarget as HTMLButtonElement).style.color = "var(--color-primary)";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLButtonElement).style.borderColor = "var(--color-border)";
              (e.currentTarget as HTMLButtonElement).style.color = "var(--color-muted-foreground)";
            }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

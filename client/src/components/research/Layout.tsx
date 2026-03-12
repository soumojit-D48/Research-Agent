import Link from "next/link";
import { usePathname } from "next/navigation";
import { Search, Clock, BookOpen, Cpu } from "lucide-react";

const nav = [
  { to: "/", label: "Research", icon: Search },
  { to: "/history", label: "History", icon: Clock },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-dvh flex flex-col" style={{ backgroundColor: "var(--color-background)", color: "var(--color-foreground)" }}>
      {/* Header */}
      <header
        className="sticky top-0 z-50 border-b flex items-center justify-between px-6 py-3"
        style={{
          backgroundColor: "color-mix(in srgb, var(--color-background) 85%, transparent)",
          backdropFilter: "blur(12px)",
          borderColor: "var(--color-border)",
        }}
      >
        <Link href="/" className="flex items-center gap-2 group">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: "var(--color-primary)", boxShadow: "var(--shadow-glow-sm)" }}
          >
            <Cpu size={16} style={{ color: "var(--color-primary-foreground)" }} />
          </div>
          <span className="font-semibold tracking-tight" style={{ fontSize: "1rem" }}>
            Research<span style={{ color: "var(--color-primary)" }}>AI</span>
          </span>
        </Link>

        <nav className="flex items-center gap-1">
          {nav.map(({ to, label, icon: Icon }) => {
            const active = pathname === to;
            return (
              <Link
                key={to}
                href={to}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200"
                style={{
                  backgroundColor: active ? "var(--color-accent)" : "transparent",
                  color: active ? "var(--color-primary)" : "var(--color-muted-foreground)",
                }}
              >
                <Icon size={14} />
                {label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" style={{ backgroundColor: "var(--color-muted)", color: "var(--color-muted-foreground)" }}>
          <BookOpen size={11} />
          AI Research Agent
        </div>
      </header>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        {children}
      </main>
    </div>
  );
}

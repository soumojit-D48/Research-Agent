"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Brain, History, Home } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Home", icon: Home },
  { href: "/history", label: "History", icon: History },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 border-b"
      style={{
        backgroundColor: "color-mix(in srgb, var(--color-background) 90%, transparent)",
        backdropFilter: "blur(12px)",
        borderColor: "var(--color-border)",
      }}
    >
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: "var(--color-primary)" }}
          >
            <Brain size={16} style={{ color: "var(--color-primary-foreground)" }} />
          </div>
          <span
            className="font-semibold text-sm"
            style={{ color: "var(--color-foreground)" }}
          >
            Research Agent
          </span>
        </Link>

        <div className="flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-all",
                  "hover:bg-opacity-50"
                )}
                style={{
                  backgroundColor: isActive ? "var(--color-muted)" : "transparent",
                  color: isActive
                    ? "var(--color-foreground)"
                    : "var(--color-muted-foreground)",
                }}
              >
                <Icon size={15} />
                <span className="hidden sm:inline">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}

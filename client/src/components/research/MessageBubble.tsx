import { Bot, User } from "lucide-react";
import type { Message } from "@/lib/api";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      className="flex gap-3 animate-slide-up"
      style={{ justifyContent: isUser ? "flex-end" : "flex-start" }}
    >
      {!isUser && (
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"
          style={{ backgroundColor: "var(--color-primary)", boxShadow: "var(--shadow-glow-sm)" }}
        >
          <Bot size={14} style={{ color: "var(--color-primary-foreground)" }} />
        </div>
      )}

      <div
        className="max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed"
        style={
          isUser
            ? {
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
                borderBottomRightRadius: "4px",
              }
            : {
                backgroundColor: "var(--color-card)",
                border: "1px solid var(--color-border)",
                color: "var(--color-foreground)",
                borderBottomLeftRadius: "4px",
              }
        }
      >
        <p style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{message.content}</p>
      </div>

      {isUser && (
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"
          style={{ backgroundColor: "var(--color-secondary)" }}
        >
          <User size={14} style={{ color: "var(--color-secondary-foreground)" }} />
        </div>
      )}
    </div>
  );
}

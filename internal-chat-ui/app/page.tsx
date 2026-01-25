"use client";

import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setLoading(true);

    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      setLoading(false);
      return;
    }

    const data = await res.json();

    setMessages((prev) => [
      ...prev,
      {
        role: "bot",
        text: data.answer,
        sources: data.sources || [],
      },
    ]);

    setQuestion("");
    setLoading(false);
  };

  return (
    <main
      style={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#fff5f5", // very light red
        fontFamily: "Inter, Arial, sans-serif",
      }}
    >
      {/* Header */}
      <header
        style={{
          textAlign: "center",
          padding: "28px",
          fontSize: "30px",
          fontWeight: 700,
          color: "#7f1d1d", // dark red
          backgroundColor: "#ffffff",
          borderBottom: "2px solid #fecaca",
        }}
      >
        🏢 Internal Company Chatbot
      </header>

      {/* Chat Area */}
      <div
        style={{
          flex: 1,
          padding: "32px 64px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "18px",
        }}
      >
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              justifyContent: m.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                maxWidth: "65%",
                padding: "14px 18px",
                borderRadius: "18px",
                backgroundColor:
                  m.role === "user" ? "#b91c1c" : "#ffffff",
                color:
                  m.role === "user" ? "#ffffff" : "#1f2937",
                boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
              }}
            >
              <div style={{ whiteSpace: "pre-wrap", fontSize: "15px" }}>
                {m.text}
              </div>

              {m.sources?.length > 0 && (
                <div
                  style={{
                    marginTop: 10,
                    fontSize: 12,
                    color: "#6b7280",
                  }}
                >
                  Sources:
                  <ul style={{ paddingLeft: 18, marginTop: 6 }}>
                    {m.sources.map((s: any, idx: number) => (
                      <li key={idx}>
                        {s.document}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ color: "#7f1d1d", fontSize: 14 }}>
            Bot is thinking…
          </div>
        )}
      </div>

      {/* Input Box */}
      <div
        style={{
          padding: "24px 64px 32px",
          backgroundColor: "#ffffff",
          borderTop: "2px solid #fecaca",
          display: "flex",
          gap: "16px",
        }}
      >
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          placeholder="Type your question here..."
          style={{
            flex: 1,
            padding: "16px 18px",
            fontSize: "16px",
            borderRadius: "14px",
            border: "1px solid #fca5a5",
            outline: "none",
            color: "#111827", // DARK text while typing
          }}
        />
        <button
          onClick={askQuestion}
          style={{
            padding: "0 28px",
            borderRadius: "14px",
            backgroundColor: "#b91c1c",
            color: "#ffffff",
            fontSize: "16px",
            fontWeight: 600,
            border: "none",
            cursor: "pointer",
          }}
        >
          Ask
        </button>
      </div>
    </main>
  );
}

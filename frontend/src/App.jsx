import { useState, useEffect } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const [expandedSources, setExpandedSources] = useState({});

  const checkHealth = async () => {
    try {
      const res = await fetch(`${API_BASE}/`);
      if (res.ok) {
        setIsOnline(true);
      } else {
        setIsOnline(false);
      }
    } catch (e) {
      setIsOnline(false);
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const toggleSources = (index) => {
    setExpandedSources((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
          sources: data.sources || [],
        },
      ]);
      setIsOnline(true);
    } catch (error) {
      setIsOnline(false);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the backend server. Please make sure the FastAPI server is running.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">I</div>
          <div>
            <h1>IITD Assistant</h1>
            <span>AI assistant for IIT Delhi • Llama 3.1 8B</span>
          </div>
        </div>

        <div className="status">
          <span className={`status-dot ${isOnline ? "" : "offline"}`}></span>
          {isOnline ? "Online" : "Offline"}
        </div>
      </header>

      <main className="chat">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">✦</div>
            <h2>How can I help you today?</h2>
            <p>
              Ask questions about IIT Delhi academics, courses, CAIC guidelines, hostels, or campus life with verified document citations.
            </p>

            <div className="suggestions">
              <button
                onClick={() =>
                  setMessage("What is CAIC at IIT Delhi?")
                }
              >
                What is CAIC?
              </button>

              <button
                onClick={() =>
                  setMessage("Tell me about Engineering Physics at IIT Delhi")
                }
              >
                Engineering Physics
              </button>

              <button
                onClick={() =>
                  setMessage("What are the academic rules and grading system?")
                }
              >
                Grading System
              </button>
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="avatar">
                  {msg.role === "user" ? "You" : "IITD"}
                </div>

                <div className="message-body">
                  <div className="message-content">{msg.content}</div>

                  {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
                    <div className="sources-container">
                      <button
                        className="sources-toggle"
                        onClick={() => toggleSources(index)}
                      >
                        📚 {expandedSources[index] ? "Hide" : "View"} Top {msg.sources.length} Cited Sources
                      </button>

                      {expandedSources[index] && (
                        <div className="sources-list">
                          {msg.sources.map((src) => (
                            <div key={src.id} className="source-card">
                              <div className="source-header">
                                <span className="source-badge id-badge">
                                  [Source {src.id}]
                                </span>
                                <span className="source-badge file-badge">
                                  📄 {src.file}
                                </span>
                                <span className="source-badge page-badge">
                                  Pg {src.page}
                                </span>
                                {src.score !== undefined && (
                                  <span className="source-badge score-badge">
                                    🎯 {src.score}% Match
                                  </span>
                                )}
                              </div>
                              <div className="source-text">{src.text}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <div className="avatar">IITD</div>
                <div className="typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <div className="input-container">
        <div className="input-box">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask IITD Assistant..."
          />

          <button onClick={sendMessage} disabled={loading || !message.trim()}>
            ↑
          </button>
        </div>

        <p className="disclaimer">
          IITD Assistant powered by Llama 3.1 8B & RAG ChromaDB. Verified with source citations.
        </p>
      </div>
    </div>
  );
}

export default App;
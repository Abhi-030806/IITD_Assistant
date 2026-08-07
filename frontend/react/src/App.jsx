
import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

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
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I couldn't connect to the server.",
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
            <span>AI assistant for IIT Delhi</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Online
        </div>
      </header>


      <main className="chat">

        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">✦</div>

            <h2>How can I help you?</h2>

            <p>
              Ask me anything about IIT Delhi, academics,
              courses, projects, or campus life.
            </p>

            <div className="suggestions">
              <button
                onClick={() =>
                  setMessage("Tell me about Engineering Physics at IIT Delhi")
                }
              >
                Engineering Physics
              </button>

              <button
                onClick={() =>
                  setMessage("What are the important courses in 2nd year?")
                }
              >
                Courses
              </button>

              <button
                onClick={() =>
                  setMessage("How can I prepare for internships?")
                }
              >
                Internships
              </button>
            </div>
          </div>
        ) : (

          <div className="messages">

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.role}`}
              >
                <div className="avatar">
                  {msg.role === "user" ? "You" : "I"}
                </div>

                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <div className="avatar">I</div>

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

          <button
            onClick={sendMessage}
            disabled={loading || !message.trim()}
          >
            ↑
          </button>

        </div>

        <p className="disclaimer">
          IITD Assistant can make mistakes. Verify important information.
        </p>

      </div>

    </div>
  );
}

export default App;
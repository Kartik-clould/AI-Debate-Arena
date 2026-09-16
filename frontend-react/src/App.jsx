import { useState } from "react";
import "./App.css";

function formatText(text) {
  return text
    // Remove markdown bold
    .replace(/\*\*(.*?)\*\*/g, "$1")

    // Remove markdown italic
    .replace(/\*(.*?)\*/g, "$1")

    // Remove markdown headings
    .replace(/^#{1,6}\s*/gm, "")

    // Remove markdown table separator lines
    .replace(/^\s*\|?[\s:-]+\|[\s|:-]*\|?\s*$/gm, "")

    // Remove table pipes
    .replace(/\|/g, " ")

    // Convert <br> into a new line
    .replace(/<br\s*\/?>/gi, "\n")

    // Remove escaped markdown characters
    .replace(/\\([*#|])/g, "$1")

    // Clean excessive spaces
    .replace(/[ \t]+/g, " ")

    // Clean excessive blank lines
    .replace(/\n{3,}/g, "\n\n")

    .trim();
}


function DebateCard({ title, text, type }) {
  const [expanded, setExpanded] = useState(false);

  const cleanText = formatText(text);

  const preview = cleanText.length > 700
    ? cleanText.substring(0, 700) + "..."
    : cleanText;

  return (
    <div className={`agent-card ${type}`}>

      <h2>{title}</h2>

      <h3>
        {title.includes("REBUTTAL")
          ? "Rebuttal"
          : "Opening Argument"}
      </h3>

      <div className="argument-text">
        {expanded ? cleanText : preview}
      </div>

      {cleanText.length > 700 && (
        <button
          className="read-more"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? "Show Less ▲" : "Read More ▼"}
        </button>
      )}

    </div>
  );
}
function App() {

  const [topic, setTopic] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function startDebate() {

    if (topic.trim() === "") {
      alert("Please enter a debate topic.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {

      const response = await fetch("https://ai-debate-arena-lmai.onrender.com/debate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          topic: topic
        })
      });

      const data = await response.json();

      setResult(data);

    } catch (error) {

      alert("Could not connect to the FastAPI server.");

    }

    setLoading(false);
  }

  return (
    <div className="app">

      <h1>AI Debate Arena</h1>

      <p className="subtitle">
        Multi-Agent Debate System with ANN Evaluation
      </p>

      <div className="topic-box">

        <input
          type="text"
          placeholder="Enter your debate topic..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />

        <button onClick={startDebate}>
          Start Debate
        </button>

      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>AI agents are debating...</p>
          <span>Please wait while the debate is being generated.</span>
        </div>
      )}

      {result && (

        <div className="debate-section">

          <div className="topic-display">
            <span>DEBATE TOPIC</span>
<h2>{result.topic.replace(/^#+\s*/, "")}</h2>
          </div>

          <h2 className="section-title">
            Debate Transcript
          </h2>

          <div className="debate-area">


            <DebateCard
              title="🔵 PRO AGENT"
              text={result.pro_argument}
              type="pro-card"
            />

            <DebateCard
              title="🔴 CON AGENT"
              text={result.con_argument}
              type="con-card"
            />

            <DebateCard
              title="🔵 PRO REBUTTAL"
              text={result.pro_reply}
              type="pro-card"
            />

            <DebateCard
              title="🔴 CON REBUTTAL"
              text={result.con_reply}
              type="con-card"
            />

          </div>
                  <div className="judge-section">

  <h2 className="section-title">
    Judge Evaluation
  </h2>

  <div className="scores-grid">

    <div className="score-card pro-score">
      <h3>🔵 PRO AGENT</h3>

      <p>
        <span className="score-label">Quality</span>
        <span>{result.judge_scores[0]}/10</span>
      </p>

      <p>
        <span className="score-label">Relevance</span>
        <span>{result.judge_scores[1]}/10</span>
      </p>

      <p>
        <span className="score-label">Reasoning</span>
        <span>{result.judge_scores[2]}/10</span>
      </p>
    </div>

    <div className="score-card con-score">
      <h3>🔴 CON AGENT</h3>

      <p>
        <span className="score-label">Quality</span>
        <span>{result.judge_scores[3]}/10</span>
      </p>

      <p>
        <span className="score-label">Relevance</span>
        <span>{result.judge_scores[4]}/10</span>
      </p>

      <p>
        <span className="score-label">Reasoning</span>
        <span>{result.judge_scores[5]}/10</span>
      </p>
    </div>

  </div>

<div className="ann-section">

  <h2 className="section-title">
    ANN Final Evaluation
  </h2>

  <div className="winner-card">

    <p className="ann-label">
      PREDICTED WINNER
    </p>

    <h1 className="winner">
      🏆 {result.winner} WINS
    </h1>

    <p className="ann-description">
      The winner was predicted by the Artificial Neural Network
      using the six scores given by the AI Judge.
    </p>

    <div className="probability-grid">

      <div className="probability-card pro-probability">
        <h3>🔵 PRO</h3>

        <div className="probability">
          {(result.pro_probability * 100).toFixed(1)}%
        </div>

        <p>Winning Probability</p>
      </div>

      <div className="probability-card con-probability">
        <h3>🔴 CON</h3>

        <div className="probability">
          {(result.con_probability * 100).toFixed(1)}%
        </div>

        <p>Winning Probability</p>
      </div>

    </div>

  </div>

</div>

</div>
        </div>

      )}

    </div>
  );
}

export default App;
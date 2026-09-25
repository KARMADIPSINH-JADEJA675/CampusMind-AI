import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/chat";

const quickActions = [
  {
    icon: "📅",
    title: "My Timetable",
    message: "What is my timetable for Monday?",
  },
  {
    icon: "📢",
    title: "Campus Notices",
    message: "What are the latest campus notices and announcements?",
  },
  {
    icon: "💼",
    title: "Placements",
    message: "What placement opportunities are available?",
  },
  {
    icon: "📚",
    title: "Study Notes",
    message: "Give me study notes about DBMS normalization.",
  },
  {
    icon: "🧠",
    title: "Generate Quiz",
    message: "Create 5 multiple choice questions about DBMS normalization.",
  },
];

/* =========================================================
   INTENT DETECTION
========================================================= */

function detectIntent(message) {
  const text = message.toLowerCase();

  if (
    text.includes("timetable") ||
    text.includes("schedule") ||
    text.includes("class")
  ) {
    return {
      label: "Timetable",
      icon: "📅",
      tool: "get_timetable",
    };
  }

  if (
    text.includes("notice") ||
    text.includes("announcement") ||
    text.includes("event")
  ) {
    return {
      label: "Campus Updates",
      icon: "📢",
      tool: "get_notices",
    };
  }

  if (
    text.includes("placement") ||
    text.includes("job") ||
    text.includes("recruitment") ||
    text.includes("company")
  ) {
    return {
      label: "Placement Search",
      icon: "💼",
      tool: "get_placements",
    };
  }

  if (
    text.includes("quiz") ||
    text.includes("question") ||
    text.includes("mcq")
  ) {
    return {
      label: "Quiz Generation",
      icon: "🧠",
      tool: "generate_quiz",
    };
  }

  if (
    text.includes("notes") ||
    text.includes("study") ||
    text.includes("dbms") ||
    text.includes("normalization")
  ) {
    return {
      label: "Study / Learning",
      icon: "📚",
      tool: "search_notes",
    };
  }

  return {
    label: "Campus Assistant",
    icon: "🤖",
    tool: "AI Assistant",
  };
}

/* =========================================================
   QUIZ PARSER
========================================================= */

function parseQuiz(text) {
  const questions = [];

  if (!text) return questions;

  const questionRegex =
    /(?:\*\*Q(\d+)\.\s*([\s\S]*?)\*\*|Q(\d+)\.\s*([^\n]+))/g;

  const matches = [...text.matchAll(questionRegex)];

  matches.forEach((match, index) => {
    const number = match[1] || match[3] || index + 1;

    const questionText = (
      match[2] ||
      match[4] ||
      ""
    )
      .trim()
      .replace(/\*\*/g, "");

    const start = match.index + match[0].length;

    const nextStart =
      index + 1 < matches.length
        ? matches[index + 1].index
        : text.length;

    const block = text.slice(start, nextStart);

    const optionRegex =
      /(?:-\s*)?(?:\*\*)?\(([A-D])\)(?:\*\*)?\s*([^\n]+)/g;

    const options = [...block.matchAll(optionRegex)].map(
      (option) => ({
        letter: option[1].toUpperCase(),
        text: option[2]
          .trim()
          .replace(/\*\*/g, ""),
      })
    );

    const answerMatch = block.match(
      /Correct\s*Answer:\*?\*?\s*Option\s*([A-D])/i
    );

    const explanationMatch = block.match(
      /Explanation:\*?\*?\s*([\s\S]*)/i
    );

    if (questionText && options.length >= 2) {
      questions.push({
        number,
        question: questionText,
        options,
        answer: answerMatch
          ? answerMatch[1].toUpperCase()
          : null,
        explanation: explanationMatch
          ? explanationMatch[1]
            .trim()
            .replace(/\*\*/g, "")
          : "",
      });
    }
  });

  return questions;
}

/* =========================================================
   INTERACTIVE QUIZ
========================================================= */

function InteractiveQuiz({
  content,
  onQuizComplete,
}) {
  const questions = parseQuiz(content);

  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);
  const [score, setScore] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [finished, setFinished] = useState(false);

  if (!questions.length) {
    return (
      <div className="message-bubble">
        {content}
      </div>
    );
  }

  const question = questions[current];

  const submitAnswer = () => {
    if (!selected || submitted) return;

    setSubmitted(true);

    if (selected === question.answer) {
      setScore((previous) => previous + 1);
    }
  };

  const nextQuestion = () => {
    if (current + 1 >= questions.length) {
      const finalScore =
        score +
        (selected === question.answer ? 1 : 0);

      setFinished(true);

      onQuizComplete(
        finalScore,
        questions.length
      );

      return;
    }

    setCurrent((previous) => previous + 1);
    setSelected(null);
    setSubmitted(false);
  };

  const restartQuiz = () => {
    setCurrent(0);
    setSelected(null);
    setScore(0);
    setSubmitted(false);
    setFinished(false);
  };

  if (finished) {
    const percentage = Math.round(
      (score / questions.length) * 100
    );

    return (
      <div className="quiz-card quiz-result">
        <div className="quiz-result-icon">
          {percentage >= 80
            ? "🏆"
            : percentage >= 50
              ? "🎉"
              : "📚"}
        </div>

        <h2>Quiz Completed!</h2>

        <div className="quiz-score">
          {score} / {questions.length}
        </div>

        <p>
          You answered {score} out of{" "}
          {questions.length} questions correctly.
        </p>

        <div className="quiz-percentage">
          {percentage}% Score
        </div>

        <button
          className="quiz-button"
          onClick={restartQuiz}
        >
          🔄 Retry Quiz
        </button>
      </div>
    );
  }

  return (
    <div className="quiz-card">
      <div className="quiz-top">
        <span className="quiz-label">
          🧠 INTERACTIVE QUIZ
        </span>

        <span className="quiz-progress">
          {current + 1} / {questions.length}
        </span>
      </div>

      <div className="quiz-progress-bar">
        <div
          style={{
            width: `${((current + 1) /
                questions.length) *
              100
              }%`,
          }}
        />
      </div>

      <h3>
        Q{question.number}.{" "}
        {question.question}
      </h3>

      <div className="quiz-options">
        {question.options.map((option) => {
          const isSelected =
            selected === option.letter;

          const isCorrect =
            submitted &&
            option.letter === question.answer;

          const isWrong =
            submitted &&
            isSelected &&
            option.letter !== question.answer;

          return (
            <button
              key={option.letter}
              className={`quiz-option ${isSelected
                  ? "selected"
                  : ""
                } ${isCorrect
                  ? "correct"
                  : ""
                } ${isWrong
                  ? "wrong"
                  : ""
                }`}
              onClick={() => {
                if (!submitted) {
                  setSelected(
                    option.letter
                  );
                }
              }}
              disabled={submitted}
            >
              <span className="option-letter">
                {option.letter}
              </span>

              <span className="option-text">
                {option.text}
              </span>

              {isCorrect && (
                <span>✓</span>
              )}

              {isWrong && (
                <span>✕</span>
              )}
            </button>
          );
        })}
      </div>

      {submitted && (
        <div
          className={`quiz-feedback ${selected === question.answer
              ? "correct"
              : "wrong"
            }`}
        >
          <strong>
            {selected === question.answer
              ? "🎉 Correct!"
              : "❌ Incorrect"}
          </strong>

          {selected !== question.answer &&
            question.answer && (
              <p>
                Correct answer:{" "}
                <strong>
                  {question.answer}
                </strong>
              </p>
            )}

          {question.explanation && (
            <p>
              {question.explanation}
            </p>
          )}
        </div>
      )}

      <div className="quiz-footer">
        <span>
          Score:{" "}
          <strong>{score}</strong>
        </span>

        {!submitted ? (
          <button
            className="quiz-button"
            onClick={submitAnswer}
            disabled={!selected}
          >
            Submit Answer
          </button>
        ) : (
          <button
            className="quiz-button"
            onClick={nextQuestion}
          >
            {current + 1 ===
              questions.length
              ? "Finish Quiz"
              : "Next Question →"}
          </button>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   STUDENT INTELLIGENCE DASHBOARD
========================================================= */

function StudentProgress({
  progress,
}) {
  const bestScore =
    progress.bestScore || 0;

  const learningLevel =
    bestScore >= 80
      ? "Advanced Learner"
      : bestScore >= 60
        ? "Growing Strong"
        : bestScore > 0
          ? "Keep Practicing"
          : "Ready to Learn";

  return (
    <section className="student-progress">

      <div className="progress-heading">
        <div>
          <span className="progress-eyebrow">
            🎯 STUDENT INTELLIGENCE
          </span>

          <h2>
            Your Learning Progress
          </h2>

          <p>
            Track your campus learning
            activity and quiz performance.
          </p>
        </div>

        <div className="learning-level">
          <span>✨</span>
          {learningLevel}
        </div>
      </div>

      <div className="progress-stats">

        <div className="progress-stat">
          <div className="stat-icon">
            🧠
          </div>

          <div>
            <strong>
              {progress.quizzesTaken}
            </strong>

            <span>
              Quizzes Taken
            </span>
          </div>
        </div>

        <div className="progress-stat">
          <div className="stat-icon">
            🏆
          </div>

          <div>
            <strong>
              {bestScore}%
            </strong>

            <span>
              Best Score
            </span>
          </div>
        </div>

        <div className="progress-stat">
          <div className="stat-icon">
            📚
          </div>

          <div>
            <strong>
              {progress.topicsPracticed}
            </strong>

            <span>
              Topics Practiced
            </span>
          </div>
        </div>

        <div className="progress-stat">
          <div className="stat-icon">
            🔥
          </div>

          <div>
            <strong>
              {progress.streak}
            </strong>

            <span>
              Day Streak
            </span>
          </div>
        </div>

      </div>

      <div className="progress-bottom">

        <div className="progress-meter">

          <div className="meter-header">
            <span>
              Learning Progress
            </span>

            <strong>
              {bestScore}%
            </strong>
          </div>

          <div className="meter">
            <div
              style={{
                width: `${bestScore}%`,
              }}
            />
          </div>

        </div>

        <div className="recommendation">

          <span className="recommendation-icon">
            💡
          </span>

          <div>
            <small>
              NEXT RECOMMENDATION
            </small>

            <strong>
              Practice Functional
              Dependencies
            </strong>
          </div>

        </div>

      </div>

    </section>
  );
}

/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [messages, setMessages] =
    useState([]);

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [progress, setProgress] =
    useState({
      quizzesTaken: 0,
      bestScore: 0,
      topicsPracticed: 0,
      streak: 1,
    });

  const [activity, setActivity] =
    useState({
      visible: false,
      intent: "Campus Assistant",
      intentIcon: "🤖",
      tool: null,
      status: "Ready",
      steps: [],
    });

  /* =======================================================
     QUIZ COMPLETE
  ======================================================= */

  const handleQuizComplete = (
    score,
    total
  ) => {
    const percentage =
      total > 0
        ? Math.round(
          (score / total) * 100
        )
        : 0;

    setProgress((previous) => ({
      quizzesTaken:
        previous.quizzesTaken + 1,

      bestScore: Math.max(
        previous.bestScore,
        percentage
      ),

      topicsPracticed: Math.max(
        previous.topicsPracticed,
        1
      ),

      streak: previous.streak,
    }));
  };

  /* =======================================================
     SEND MESSAGE
  ======================================================= */

  const sendMessage = async (
    messageText = input
  ) => {
    const message =
      messageText.trim();

    if (!message || loading) {
      return;
    }

    const detected =
      detectIntent(message);

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setLoading(true);

    setActivity({
      visible: true,
      intent: detected.label,
      intentIcon: detected.icon,
      tool: detected.tool,
      status: "Processing",
      steps: [
        {
          icon: "✓",
          text: "Request received",
          done: true,
        },
        {
          icon: "⚡",
          text: `Intent detected: ${detected.label}`,
          done: true,
        },
        {
          icon: "🔌",
          text: `Connecting to MCP tool: ${detected.tool}`,
          done: false,
        },
        {
          icon: "⏳",
          text: "Waiting for tool response...",
          done: false,
        },
      ],
    });

    try {
      const response =
        await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            message,
            student_id: "std_001",
            session_id: "default",
          }),
        });

      if (!response.ok) {
        throw new Error(
          `Server error: ${response.status}`
        );
      }

      const data =
        await response.json();

      const actualTool =
        data.mcp_tool_used ||
        detected.tool;

      const actualStatus =
        data.mcp_metadata?.status ||
        "success";

      setActivity({
        visible: true,
        intent: detected.label,
        intentIcon: detected.icon,
        tool: actualTool,
        status: actualStatus,
        steps: [
          {
            icon: "✓",
            text: "Request received",
            done: true,
          },
          {
            icon: "✓",
            text: `Intent detected: ${detected.label}`,
            done: true,
          },
          {
            icon: "✓",
            text: `MCP tool executed: ${actualTool}`,
            done: true,
          },
          {
            icon: "✓",
            text: "Response received successfully",
            done: true,
          },
        ],
      });

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            data.reply ||
            "No response received.",
          tool: actualTool,
          status: actualStatus,
        },
      ]);
    } catch (error) {
      console.error(error);

      setActivity({
        visible: true,
        intent: detected.label,
        intentIcon: detected.icon,
        tool: detected.tool,
        status: "error",
        steps: [
          {
            icon: "✓",
            text: "Request received",
            done: true,
          },
          {
            icon: "✓",
            text: `Intent detected: ${detected.label}`,
            done: true,
          },
          {
            icon: "✕",
            text: "Unable to connect to MCP/backend",
            done: false,
          },
        ],
      });

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Unable to connect to CampusMind AI backend. Please make sure FastAPI and MCP server are running.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            🧠
          </div>

          <div>
            <h2>CampusMind</h2>
            <span>
              AI Assistant
            </span>
          </div>

        </div>

        <nav className="nav">

          <button className="nav-item active">
            <span>🤖</span>
            AI Assistant
          </button>

          <button
            className="nav-item"
            onClick={() =>
              sendMessage(
                "What is my timetable for Monday?"
              )
            }
          >
            <span>📅</span>
            Timetable
          </button>

          <button
            className="nav-item"
            onClick={() =>
              sendMessage(
                "What are the latest campus notices and announcements?"
              )
            }
          >
            <span>📢</span>
            Notices
          </button>

          <button
            className="nav-item"
            onClick={() =>
              sendMessage(
                "What placement opportunities are available?"
              )
            }
          >
            <span>💼</span>
            Placements
          </button>

          <button
            className="nav-item"
            onClick={() =>
              sendMessage(
                "Give me study notes about DBMS normalization."
              )
            }
          >
            <span>📚</span>
            Study Notes
          </button>

          <button
            className="nav-item"
            onClick={() =>
              sendMessage(
                "Create 5 multiple choice questions about DBMS normalization."
              )
            }
          >
            <span>🧠</span>
            Quiz
          </button>

        </nav>

        <div className="sidebar-bottom">

          <div className="mcp-status">
            <span className="status-dot"></span>
            MCP Connected
          </div>

          <div className="student-card">

            <div className="avatar">
              K
            </div>

            <div>
              <strong>
                Student
              </strong>

              <small>
                ID: std_001
              </small>
            </div>

          </div>

        </div>

      </aside>

      {/* MAIN */}

      <main className="main">

        {/* HEADER */}

        <header className="header">

          <div>

            <p className="eyebrow">
              CAMPUSMIND AI
            </p>

            <h1>
              Good evening 👋
            </h1>

            <p className="subtitle">
              Your intelligent campus assistant
            </p>

          </div>

          <div className="connection">

            <span className="status-dot"></span>

            MCP Connected

          </div>

        </header>

        {/* STUDENT INTELLIGENCE */}

        <StudentProgress
          progress={progress}
        />

        {/* LIVE MCP ACTIVITY */}

        {activity.visible && (
          <section className="activity-panel">

            <div className="activity-header">

              <div>

                <span className="activity-label">
                  ⚡ LIVE AI ACTIVITY
                </span>

                <h3>
                  {activity.intentIcon}{" "}
                  {activity.intent}
                </h3>

              </div>

              <span
                className={`activity-status ${activity.status ===
                    "error"
                    ? "error"
                    : "success"
                  }`}
              >
                ● {activity.status}
              </span>

            </div>

            <div className="activity-tool">

              <span>🔌</span>

              <div>

                <small>
                  MCP TOOL
                </small>

                <strong>
                  {activity.tool ||
                    "Detecting..."}
                </strong>

              </div>

            </div>

            <div className="activity-steps">

              {activity.steps.map(
                (step, index) => (
                  <div
                    className="activity-step"
                    key={index}
                  >

                    <span
                      className={`step-icon ${step.done
                          ? "done"
                          : "waiting"
                        }`}
                    >
                      {step.icon}
                    </span>

                    <span>
                      {step.text}
                    </span>

                  </div>
                )
              )}

            </div>

          </section>
        )}

        {/* CHAT */}

        <section className="chat-container">

          {messages.length === 0 ? (

            <div className="welcome">

              <div className="welcome-icon">
                🧠
              </div>

              <h2>
                How can I help you today?
              </h2>

              <p>
                Ask about your timetable,
                campus notices, placements,
                study material, or generate
                a quiz.
              </p>

              <div className="quick-actions">

                {quickActions.map(
                  (action) => (
                    <button
                      className="quick-card"
                      key={action.title}
                      onClick={() =>
                        sendMessage(
                          action.message
                        )
                      }
                    >

                      <span className="quick-icon">
                        {action.icon}
                      </span>

                      <span>

                        <strong>
                          {action.title}
                        </strong>

                        <small>
                          Ask CampusMind AI
                        </small>

                      </span>

                    </button>
                  )
                )}

              </div>

            </div>

          ) : (

            <div className="messages">

              {messages.map(
                (message, index) => (

                  <div
                    className={`message-row ${message.role}`}
                    key={index}
                  >

                    <div className="message-avatar">
                      {message.role ===
                        "user"
                        ? "K"
                        : "🧠"}
                    </div>

                    <div className="message-content">

                      {message.tool ===
                        "generate_quiz" ? (

                        <InteractiveQuiz
                          content={
                            message.content
                          }
                          onQuizComplete={
                            handleQuizComplete
                          }
                        />

                      ) : (

                        <div
                          className={`message-bubble ${message.error
                              ? "error-message"
                              : ""
                            }`}
                        >
                          {message.content}
                        </div>

                      )}

                      {message.tool && (
                        <div className="tool-info">

                          <span>
                            🔌
                          </span>

                          MCP Tool:

                          <strong>
                            {message.tool}
                          </strong>

                          {message.status && (
                            <span className="tool-status">
                              ●{" "}
                              {message.status}
                            </span>
                          )}

                        </div>
                      )}

                    </div>

                  </div>

                )
              )}

              {loading && (

                <div className="message-row assistant">

                  <div className="message-avatar">
                    🧠
                  </div>

                  <div className="message-content">

                    <div className="message-bubble typing">

                      <span></span>
                      <span></span>
                      <span></span>

                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </section>

        {/* INPUT */}

        <div className="input-area">

          <form
            onSubmit={handleSubmit}
            className="chat-form"
          >

            <input
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              placeholder="Ask anything about your campus..."
              disabled={loading}
            />

            <button
              type="submit"
              disabled={
                loading ||
                !input.trim()
              }
            >
              {loading
                ? "..."
                : "Send ➤"}
            </button>

          </form>

          <p className="input-hint">
            CampusMind AI uses MCP tools to
            provide campus-specific answers.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;
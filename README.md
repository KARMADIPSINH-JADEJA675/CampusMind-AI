# 🚀 CampusMind AI – Intelligent Campus Assistant

> **An intelligent campus assistant using Generative AI and Model Context Protocol (MCP)**

CampusMind AI is an intelligent campus assistant designed to provide students with campus information and learning support through **natural-language interaction**.

The system combines **React.js, FastAPI, Generative AI, and Model Context Protocol (MCP)** to connect students with different campus services through a single platform.

---

## 🎥 Project Demo

▶️ **YouTube Demo:**  
https://youtu.be/fNZIs5gA8DA

---

## ✨ Features

### 📅 Timetable Assistant
Students can ask natural-language questions about their timetable and retrieve the required schedule information.

### 📢 Campus Notices
Provides campus announcements and notices through the AI assistant.

### 💼 Placement Information
Students can access available placement and recruitment opportunities.

### 📚 Study Notes
Students can search for academic study material by asking questions about specific topics.

### 📝 Interactive Quiz
Generates multiple-choice questions on requested academic topics and allows students to attempt the quiz interactively.

### 📊 Student Intelligence
Provides learning-related information such as:
- Quizzes taken
- Best score
- Topics practiced
- Learning progress

### 🤖 Live AI Activity
Displays the processing activity of the AI request, including intent detection and MCP tool execution.

### 🔌 MCP Tool Integration
Campus services are divided into individual MCP tools, making the architecture modular and easier to extend.

---

# 🧠 MCP Tools

CampusMind AI currently provides five MCP tools:

| MCP Tool | Description |
|---|---|
| `get_timetable` | Retrieves student timetable information |
| `get_notices` | Retrieves campus notices and announcements |
| `get_placements` | Retrieves placement opportunities |
| `search_notes` | Searches academic study notes |
| `generate_quiz` | Generates multiple-choice questions |

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       Student        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Frontend     │
                    │      + Vite          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    │       Python         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     MCP Server       │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   get_timetable        get_notices         get_placements
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
              search_notes          generate_quiz
                    │                      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Campus Data       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Response        │
                    └──────────────────────┘

# 🔄 Working Flow

```
```

```
Student asks a question
        ↓
React Frontend receives the query
        ↓
FastAPI Backend processes the request
        ↓
Required MCP tool is identified
        ↓
MCP Server executes the tool
        ↓
Campus data is retrieved
        ↓
Response is returned to the student
```

---

# 🛠️ Technology Stack

## Frontend

-  React.js 
-  Vite 
-  JavaScript 
-  CSS 

## Backend

-  Python 
-  FastAPI 

## AI & Integration

-  Generative AI 
-  Model Context Protocol (MCP) 

## Data

-  JSON-based campus data 
-  Timetable data 
-  Notices data 
-  Placement data 
-  Study notes 
-  Student data 

---

# 📂 Project Structure

```
```

```
CampusMind-AI/
│
├── backend/
│   └── app/
│       ├── database/
│       ├── middleware/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       └── main.py
│
├── frontend/
│
├── mcp-server/
│   ├── server.py
│   └── tools/
│       ├── notes.py
│       ├── notices.py
│       ├── placements.py
│       ├── quiz.py
│       └── timetable.py
│
├── data/
│   ├── timetable.json
│   ├── notices.json
│   ├── placements.json
│   ├── notes.json
│   └── students.json
│
├── rag/
│
├── docs/
│
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```
```

```
git clone https://github.com/KARMADIPSINH-JADEJA675/CampusMind-AI.git
cd CampusMind-AI
```

---

## 2. Backend Setup

Create a Python virtual environment:

```
```

```
python -m venv venv
```

### Windows

```
```

```
venv\Scripts\activate
```

Install dependencies:

```
```

```
pip install -r backend\requirements.txt
```

Configure the required environment variables using:

```
```

```
.env.example
```

Start the FastAPI backend:

```
```

```
cd backend
python -m uvicorn app.main:app --reload
```

Backend:

```
```

```
http://127.0.0.1:8000
```

FastAPI Documentation:

```
```

```
http://127.0.0.1:8000/docs
```

---

## 3. Start MCP Server

Open another terminal:

```
```

```
cd mcp-server
python server.py
```

The MCP server provides the campus-specific tools used by the application.

---

## 4. Frontend Setup

Open another terminal:

```
```

```
cd frontend
npm install
npm run dev
```

Open the application:

```
```

```
http://localhost:5173
```

---

# 💬 Example Queries

### Timetable

```
```

```
What is my timetable for Monday?
```

### Notices

```
```

```
What are the latest campus notices and announcements?
```

### Placements

```
```

```
What placement opportunities are available?
```

### Study Notes

```
```

```
Give me study notes about DBMS normalization.
```

### Quiz

```
```

```
Create 5 multiple choice questions about DBMS normalization.
```

---

# 🧪 Demonstrated MCP Workflow

For example, when the student asks:

```
```

```
Give me study notes about DBMS normalization.
```

The workflow is:

```
```

```
Student Query
     ↓
React Frontend
     ↓
FastAPI Backend
     ↓
Intent Detection
     ↓
search_notes MCP Tool
     ↓
Study Notes Data
     ↓
Response
```

For a quiz request:

```
```

```
Create 5 multiple choice questions about DBMS normalization.
```

The workflow uses:

```
```

```
generate_quiz
```

and the generated questions are displayed as an interactive quiz.

---

# 🎯 Project Objective

The main objective of CampusMind AI is to provide students with a **single intelligent platform** for accessing campus information and learning support through natural-language interaction.

Instead of checking different sources separately, students can interact with the assistant and request the required campus or academic information directly.

---

# 🔐 Environment Variables

Sensitive configuration is stored locally in the `.env` file and is **not included in the GitHub repository**.

Use:

```
```

```
.env.example
```

as the reference for configuring the required environment variables.

---

# 🚀 Future Scope

-  🎙️ Voice-based campus assistant 
-  🎯 Personalized career guidance 
-  💼 Skill-based placement matching 
-  📄 Advanced document search 
-  🧠 Personalized student recommendations 
-  🔔 Notifications and reminders 
-  🤖 Additional AI-powered campus services 
-  🔗 More MCP tools and agentic workflows 

---

# 📺 Demo Video

**CampusMind AI – Intelligent Campus Assistant**

[https://youtu.be/fNZIs5gA8DA](https://youtu.be/fNZIs5gA8DA)

---

# 🔗 Project Links

### GitHub Repository

[https://github.com/KARMADIPSINH-JADEJA675/CampusMind-AI](https://github.com/KARMADIPSINH-JADEJA675/CampusMind-AI)

### YouTube Demo

[https://youtu.be/fNZIs5gA8DA](https://youtu.be/fNZIs5gA8DA)

---

# 👨‍💻 Project

**CampusMind AI – Intelligent Campus Assistant**

Built using:

**Generative AI + React.js + FastAPI + MCP**

```
```

```
Ask → Understand → Select Tool → Retrieve Data → Respond

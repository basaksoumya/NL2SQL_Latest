# 🧠 NL2SQL Chatbot using Vanna 2.0 + FastAPI

## 📌 Project Description

This project implements an AI-powered Natural Language to SQL (NL2SQL) system using **Vanna AI 2.0** and **FastAPI**.

Users can ask questions in plain English, and the system:

* Converts them into SQL queries using an LLM (Google Gemini)
* Executes the query on a SQLite database
* Returns structured results

The system focuses on **accuracy, robustness, and clean architecture**, with proper handling of edge cases and SQL validation.

---

## ⚙️ Tech Stack

* Python 3.10+
* Vanna AI 2.0
* FastAPI
* SQLite
* Google Gemini (gemini-2.5-flash)
* Pandas

---

## 🚀 Setup Instructions (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd nl2sql_project
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variable (Gemini API Key)

#### Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

---

## 🗄️ Database Setup

Run the following command to create the database and insert dummy data:

```bash
python setup_database.py
```

This will generate:

```
clinic.db
```

---

## 🧠 Seed Agent Memory

Run:

```bash
python seed_memory.py
```

This script preloads the agent with **15+ high-quality question–SQL pairs**, improving accuracy and handling of complex queries.

---

## ▶️ Start the API Server

```bash
python -m uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

Interactive API docs:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Documentation

### 🔹 POST `/chat`

#### Request:

```json
{
  "question": "Which city has the most patients?"
}
```

#### Response:

```json
{
  "message": "Kolkata has the highest number of patients.",
  "sql_query": "SELECT city, COUNT(*) FROM patients GROUP BY city ORDER BY COUNT(*) DESC LIMIT 1",
  "columns": ["city", "count"],
  "rows": [["Kolkata", 35]],
  "row_count": 1
}
```

---

### 🔹 GET `/health`

#### Response:

```json
{
  "status": "ok",
  "database": "connected",
  "agent_memory_items": 15
}
```

---

## 🧱 Architecture Overview

```
User (Natural Language Question)
            ↓
       FastAPI Backend
            ↓
       Vanna 2.0 Agent
   (LLM + Tools + Memory)
            ↓
     SQL Query Generation
            ↓
     SQL Validation Layer
            ↓
     SQLite Database Execution
            ↓
        Structured Response
```

---

## ⚠️ Key Features

* ✅ Natural language to SQL conversion
* ✅ Schema-aware query generation
* ✅ SQL validation (SELECT-only queries)
* ✅ Error handling for invalid queries and DB failures
* ✅ Pre-seeded memory (15+ examples)
* ✅ Clean modular architecture

---

## ⚠️ Limitations

* ❌ Chart/visualization generation is not implemented
* ❌ Complex analytical queries may sometimes require improved prompting

---

## 🧪 Testing

The system was tested with **20 benchmark questions**, including:

* Aggregations
* Joins
* Time-based queries
* Financial queries

Results are documented in:

```
RESULTS.md
```

---

## 📌 Notes

* Uses **Vanna 2.0 architecture** (Agent + Tools + Memory)
* Does NOT use deprecated Vanna 0.x APIs (vn.train, ChromaDB)
* API keys are managed via environment variables

---

## 🙌 Conclusion

This project demonstrates how modern LLM-based agents can be integrated with backend systems to build intelligent database interfaces.

It focuses on:

* Reliability
* Clean engineering practices
* Real-world query handling

---

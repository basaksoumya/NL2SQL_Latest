# 🧠 NL2SQL Chatbot using Vanna 2.0 + FastAPI

## 📌 Project Description

This project implements an AI-powered Natural Language to SQL (NL2SQL) system using **Vanna AI 2.0** and **FastAPI**.

Users can ask questions in plain English, and the system:

* Converts them into SQL queries using an LLM (Google Gemini)
* Executes the query on a SQLite database
* Returns structured results along with optional visualizations

The system is designed with **robust engineering practices**, including validation, error handling, caching, and rate limiting.

---

## ⚙️ Tech Stack

* Python 3.10+
* Vanna AI 2.0
* FastAPI
* SQLite
* Google Gemini (`gemini-2.5-flash`)
* Pandas
* Plotly

---

## 🚀 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/basaksoumya/NL2SQL_Latest.git
cd NL2SQL_Latest
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

### 4️⃣ Set API Key (Gemini)

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

---

## 🗄️ Database Setup

```bash
python setup_database.py
```

This creates:

```
clinic.db
```

---

## 🧠 Seed Agent Memory

```bash
python seed_memory.py
```

This loads **15+ high-quality question–SQL pairs** into Vanna memory.

---

## ▶️ Run API Server

```bash
python -m uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Run Test Cases

```bash
python test_cases.py
```

> ⚠️ Due to Gemini API limits, run tests in small batches or from last queries first.

---

## 📡 API Documentation

### 🔹 POST `/chat`

#### Request:

```json
{
  "question": "Show revenue by doctor"
}
```

#### Response:

```json
{
  "sql": "SELECT d.name, SUM(i.total_amount)...",
  "columns": ["name", "revenue"],
  "rows": [["Dr A", 5000], ["Dr B", 3200]],
  "count": 2,
  "chart": { "data": [...], "layout": {...} },
  "chart_type": "bar"
}
```

---

### 🔹 GET `/health`

```json
{
  "status": "ok",
  "cache_size": 3,
  "rate_limit_users": 1
}
```

---

## 🧱 Architecture Overview

```
User (Natural Language)
        ↓
FastAPI Backend (/chat)
        ↓
Vanna 2.0 Agent (LLM + Memory + Tools)
        ↓
SQL Generation
        ↓
SQL Validation Layer
        ↓
SQLite Execution
        ↓
Result Processing + Chart Generation
        ↓
API Response
```

---

## ⚠️ Key Features

* ✅ Natural language → SQL conversion
* ✅ Schema-aware query generation
* ✅ SQL validation (SELECT-only)
* ✅ Error handling (invalid SQL, DB errors, empty results)
* ✅ Agent memory with pre-seeded examples
* ✅ Plotly-based chart generation
* ✅ Query caching (performance optimization)
* ✅ Rate limiting (API protection)
* ✅ Logging (debugging & monitoring)

---

## ⚠️ Limitations

* Gemini API has strict rate limits
* Some queries may fail due to API response issues
* Chart generation is basic (first 2 columns only)

---

## 🧠 Engineering Enhancements

To improve robustness:

* 🔁 Retry logic for LLM calls
* ⏱ Delay between requests to avoid rate limits
* 💾 Caching repeated queries
* 🧹 SQL cleaning and extraction improvements

---

## 🧪 Test Coverage

* Total questions: 20
* Successfully tested: 8
* Accuracy (tested): 100%

> ⚠️ Full testing limited by API constraints

See:

```
RESULTS.md
```

---

## 🔮 Future Improvements

* Switch to Groq / Ollama for stable inference
* Advanced charting support
* Better prompt engineering
* UI frontend integration

---

## 📌 Notes

* Uses **Vanna 2.0 architecture (not legacy 0.x)**
* No ChromaDB used
* API keys handled via environment variables
* Designed for real-world constraints (API limits)

---

## 🙌 Conclusion

This project demonstrates how modern LLM-powered agents can be integrated into backend systems to build intelligent database interfaces.

It reflects:

* Strong system design
* Real-world engineering practices
* Robust handling of external API limitations

---

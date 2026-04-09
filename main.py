from fastapi import FastAPI
from pydantic import BaseModel
from vanna_setup import get_agent
from vanna.core.user import User
import sqlite3
import asyncio
import pandas as pd
import plotly.express as px
import logging
import time

# 🔥 Globals
cache = {}
last_request_time = {}

logging.basicConfig(level=logging.INFO)

app = FastAPI()

agent = get_agent()
user = User(id="default")


class Query(BaseModel):
    question: str


# 🔐 SQL Validation
def validate_sql(sql):
    if not sql:
        return False
    sql = sql.lower()
    if any(x in sql for x in ["insert", "update", "delete", "drop", "alter"]):
        return False
    return sql.strip().startswith("select")


# 🧠 Extract SQL from text
def extract_sql_from_text(chunks):
    if not chunks:
        return None

    combined = " ".join(chunks).lower()

    if "select" not in combined:
        return None

    start = combined.find("select")

    # try to cut until end
    sql = combined[start:]

    # optional cleanup
    sql = sql.split("```")[0]

    return sql.strip()


def clean_sql(sql: str) -> str:
    if not sql:
        return sql

    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    return sql.strip()


# 🤖 Collect response from agent
async def collect_sql(question):
    outputs = []
    async for chunk in agent.send_message(user, question):
        if hasattr(chunk, "simple_component") and chunk.simple_component:
            text = getattr(chunk.simple_component, "text", "")
            if text:
                outputs.append(text)
    return outputs


# 📊 Chart Generation
def generate_chart(columns, rows):
    try:
        df = pd.DataFrame(rows)

        if len(df.columns) >= 2 and len(df) > 0:
            x = df.columns[0]
            y = df.columns[1]

            fig = px.bar(df, x=x, y=y)
            return fig.to_dict(), "bar"

    except Exception:
        pass

    return None, None


@app.post("/chat")
def chat(q: Query):
    try:
        # 🔹 Input Validation
        if not q.question or not q.question.strip():
            return {"error": "Empty question"}

        if len(q.question) > 500:
            return {"error": "Question too long"}

        # 🔹 Rate Limiting
        user_id = "default"
        now = time.time()

        if user_id in last_request_time and now - last_request_time[user_id] < 1:
            return {"error": "Too many requests. Please slow down."}

        last_request_time[user_id] = now

        # 🔹 Cache Check
        if q.question in cache:
            logging.info("Cache hit")
            return cache[q.question]

        # 🔥 Schema Prompt
        schema_prompt = """
You are an expert SQL generator.

Database Schema:

patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
doctors(id, name, specialization, department, phone)
appointments(id, patient_id, doctor_id, appointment_date, status, notes)
treatments(id, appointment_id, treatment_name, cost, duration_minutes)
invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)

Rules:
- ONLY return SQL
- ONLY SELECT queries
- NO explanation
"""

        full_query = schema_prompt + "\nUser Question: " + q.question

        # 🧠 LLM Call
        def safe_collect_sql(query):
            for _ in range(3):
                try:
                    return asyncio.run(collect_sql(query))
                except Exception:
                    time.sleep(2)
            return []

        chunks = safe_collect_sql(full_query)

        logging.info(f"LLM Output: {chunks}")

        raw_sql = extract_sql_from_text(chunks)
        sql = clean_sql(raw_sql)

        if not sql:
            return {
                "error": "LLM failed to generate SQL (possible API limit)",
                "raw_output": chunks
           }

        if not validate_sql(sql):
            return {"error": "Unsafe SQL", "sql": sql}

        # 🗄 Execute SQL
        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]

        # Convert rows to list of dicts
        rows = [dict(zip(cols, row)) for row in rows]
        conn.close()

        # 📊 Chart Generation
        chart, chart_type = generate_chart(cols, rows)

        # 🧾 Prepare Response
        result = {
            "sql": sql,
            "columns": cols,
            "rows": rows,
            "count": len(rows),
            "chart": chart,
            "chart_type": chart_type
        }

        # 💾 Cache Result
        cache[q.question] = result

        # 📜 Logging
        logging.info(f"Question: {q.question}")
        logging.info(f"SQL: {sql}")
        logging.info(f"Rows returned: {len(rows)}")

        return result

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"error": str(e)}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "cache_size": len(cache),
        "rate_limit_users": len(last_request_time)
    }
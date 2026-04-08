from fastapi import FastAPI
from pydantic import BaseModel
from vanna_setup import get_agent
from vanna.core.user import User
import sqlite3
import asyncio

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
    if any(x in sql for x in ["insert","update","delete","drop"]):
        return False
    return sql.strip().startswith("select")


# 🧠 Extract SQL from text
def extract_sql_from_text(chunks):
    for text in chunks:
        if "select" in text.lower():
            return text
    return None

def clean_sql(sql: str) -> str:
    if not sql:
        return sql

    # Remove markdown ```sql ... ```
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    # Remove trailing semicolon (optional but safe)
    if sql.endswith(";"):
        sql = sql[:-1]

    return sql.strip()

# 🤖 Collect response from agent (TEXT MODE)
async def collect_sql(question):
    outputs = []
    async for chunk in agent.send_message(user, question):
        if hasattr(chunk, "simple_component") and chunk.simple_component:
            text = getattr(chunk.simple_component, "text", "")
            if text:
                outputs.append(text)
    return outputs


@app.post("/chat")
def chat(q: Query):
    try:
        if not q.question.strip():
            return {"error": "Empty question"}

        # 🔥 Strong schema prompt
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

        # 🧠 Get response
        chunks = asyncio.run(collect_sql(full_query))

        print("DEBUG:", chunks)

        raw_sql = extract_sql_from_text(chunks)
        sql = clean_sql(raw_sql)

        if not sql:
            return {"error": "No SQL generated", "debug": chunks}

        if not validate_sql(sql):
            return {"error": "Unsafe SQL", "sql": sql}

        # 🗄 Execute
        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]

        conn.close()

        return {
            "sql": sql,
            "columns": cols,
            "rows": rows,
            "count": len(rows)
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "ok"}
import requests
import time

URL = "http://127.0.0.1:8000/chat"

questions = [
    "How many patients do we have?",
    "List all doctors and their specializations",
    "Show me appointments for last month",
    "Which doctor has the most appointments?",
    "What is the total revenue?",
    "Show revenue by doctor",
    "How many cancelled appointments last quarter?",
    "Top 5 patients by spending",
    "Average treatment cost by specialization",
    "Show monthly appointment count for the past 6 months",
    "Which city has the most patients?",
    "List patients who visited more than 3 times",
    "Show unpaid invoices",
    "What percentage of appointments are no-shows?",
    "Show the busiest day of the week for appointments",
    "Revenue trend by month",
    "Average appointment duration by doctor",
    "List patients with overdue invoices",
    "Compare revenue between departments",
    "Show patient registration trend by month"
]

for i, q in enumerate(questions, 1):
    time.sleep(2)
    print(f"\nQ{i}: {q}")
    
    try:
        res = requests.post(URL, json={"question": q})
        try:
            data = res.json()
        except:
            print("Raw response:", res.text)
            continue
        
        print("SQL:", data.get("sql"))
        print("Rows:", data.get("count"))
        
    except Exception as e:
        print("Error:", str(e))
from vanna_setup import get_agent
from vanna.core.user import User

# Initialize agent and user
agent = get_agent()
user = User(id="default")


def seed_memory():
    examples = [
        # 🔹 Patient Queries
        ("How many patients do we have?",
         "SELECT COUNT(*) AS total_patients FROM patients"),

        ("List all patients",
         "SELECT first_name, last_name, city FROM patients"),

        ("Show patients from Kolkata",
         "SELECT * FROM patients WHERE city = 'Kolkata'"),

        ("Count male and female patients",
         "SELECT gender, COUNT(*) AS count FROM patients GROUP BY gender"),

        # 🔹 Doctor Queries
        ("List all doctors",
         "SELECT name, specialization FROM doctors"),

        ("Which doctor has the most appointments?",
         """SELECT d.name, COUNT(*) AS total_appointments
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            GROUP BY d.name
            ORDER BY total_appointments DESC
            LIMIT 1"""),

        # 🔹 Appointment Queries
        ("Show completed appointments",
         "SELECT * FROM appointments WHERE status = 'Completed'"),

        ("Appointments in last 3 months",
         """SELECT * FROM appointments
            WHERE appointment_date >= DATE('now', '-3 months')"""),

        # 🔹 Financial Queries
        ("What is total revenue?",
         "SELECT SUM(total_amount) AS total_revenue FROM invoices"),

        ("Show unpaid invoices",
         "SELECT * FROM invoices WHERE status != 'Paid'"),

        ("Top 5 patients by spending",
         """SELECT p.first_name, p.last_name, SUM(i.total_amount) AS total_spending
            FROM invoices i
            JOIN patients p ON p.id = i.patient_id
            GROUP BY p.id
            ORDER BY total_spending DESC
            LIMIT 5"""),

        # 🔹 Time-Based Queries
        ("Monthly appointment count",
         """SELECT strftime('%Y-%m', appointment_date) AS month,
                   COUNT(*) AS total_appointments
            FROM appointments
            GROUP BY month
            ORDER BY month"""),

        ("Revenue trend by month",
         """SELECT strftime('%Y-%m', invoice_date) AS month,
                   SUM(total_amount) AS revenue
            FROM invoices
            GROUP BY month
            ORDER BY month"""),

        # 🔹 Advanced Queries
        ("Which city has the most patients?",
         """SELECT city, COUNT(*) AS patient_count
            FROM patients
            GROUP BY city
            ORDER BY patient_count DESC
            LIMIT 1"""),

        ("Patients with more than 3 visits",
         """SELECT patient_id, COUNT(*) AS visit_count
            FROM appointments
            GROUP BY patient_id
            HAVING visit_count > 3""")
    ]

    # Save into memory
    for question, sql in examples:
        try:
            agent.memory.save_question_tool_args(
                user=user,
                question=question,
                tool_name="RunSqlTool",
                tool_args={"sql": sql.strip()}
            )
            print(f"✅ Saved: {question}")
        except Exception as e:
            print(f"❌ Error saving {question}: {e}")

    print(f"\n🎯 Total {len(examples)} Q-SQL pairs seeded successfully.")
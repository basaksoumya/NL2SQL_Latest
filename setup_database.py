import sqlite3
import random
from faker import Faker

fake = Faker()

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

tables = ["patients", "doctors", "appointments", "treatments", "invoices"]
for t in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {t}")

cursor.execute("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
)
""")

cursor.execute("""
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    department TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT,
    notes TEXT
)
""")

cursor.execute("""
CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER
)
""")

cursor.execute("""
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
)
""")

cities = ["Kolkata", "Delhi", "Mumbai", "Bangalore", "Chennai"]
specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

# Doctors
for _ in range(15):
    cursor.execute("INSERT INTO doctors VALUES (NULL,?,?,?,?)", (
        fake.name(),
        random.choice(specializations),
        "Dept",
        fake.phone_number()
    ))

# Patients
for _ in range(200):
    cursor.execute("INSERT INTO patients VALUES (NULL,?,?,?,?,?,?,?,?)", (
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.phone_number(),
        fake.date_of_birth(),
        random.choice(["M","F"]),
        random.choice(cities),
        fake.date_this_year()
    ))

# Appointments
for _ in range(500):
    cursor.execute("INSERT INTO appointments VALUES (NULL,?,?,?,?,?)", (
        random.randint(1,200),
        random.randint(1,15),
        fake.date_time_this_year(),
        random.choice(["Scheduled","Completed","Cancelled","No-Show"]),
        fake.text()
    ))

# Treatments
for _ in range(350):
    cursor.execute("INSERT INTO treatments VALUES (NULL,?,?,?,?)", (
        random.randint(1,500),
        fake.word(),
        random.uniform(50,5000),
        random.randint(10,120)
    ))

# Invoices
for _ in range(300):
    total = random.uniform(100,5000)
    paid = total if random.random()>0.5 else total*0.5
    status = "Paid" if paid==total else "Pending"

    cursor.execute("INSERT INTO invoices VALUES (NULL,?,?,?,?,?)", (
        random.randint(1,200),
        fake.date_this_year(),
        total,
        paid,
        status
    ))

conn.commit()
conn.close()

print("Database created successfully!")
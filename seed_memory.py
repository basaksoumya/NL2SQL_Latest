from vanna_setup import get_agent
from vanna.core.user import User

agent = get_agent()
user = User(id="default")

questions = [
    "How many patients?",
    "List all doctors",
    "Total revenue"
]

for q in questions:
    try:
        agent.send_message(user, q)
        print("Trained:", q)
    except Exception as e:
        print("Error:", e)
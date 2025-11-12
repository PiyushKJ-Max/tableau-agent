from fastapi import FastAPI, Request
from pydantic import BaseModel
import difflib
from datetime import datetime

app = FastAPI()

TRIGGERS = [
    "tableau creator licence",
    "need tableau desktop",
    "can i get a tableau license",
    "requesting tableau creator",
    "i want access to tableau",
    "tableau license request",
    "tableau desktop access",
    "tableau creator access"
]

FOLLOW_UP_RESPONSE = """
Are you using Tableau Desktop for the first time?
Please go to this link and raise a different access request: https://community.tableau.com/
"""

LOG_FILE = "requests.log"

class Message(BaseModel):
    text: str

def is_triggered(user_input):
    user_input = user_input.lower()
    for trigger in TRIGGERS:
        similarity = difflib.SequenceMatcher(None, user_input, trigger).ratio()
        if similarity > 0.6:
            log_request(user_input, trigger)
            return True
    return False

def log_request(user_input, matched_trigger):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User Input: \"{user_input}\" → Matched Trigger: \"{matched_trigger}\"\n")

@app.post("/message")
async def handle_message(msg: Message):
    if is_triggered(msg.text):
        return {"response": FOLLOW_UP_RESPONSE}
    else:
        return {"response": "No Tableau license request detected."}
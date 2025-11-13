from fastapi import FastAPI, Request
from datetime import datetime
import difflib

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

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    user_input = body.get("text", "")
    if is_triggered(user_input):
        return {
            "type": "message",
            "text": FOLLOW_UP_RESPONSE
        }
    else:
        return {
            "type": "message",
            "text": "No Tableau license request detected."
        }
        
        
        import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    logger.info(f"Incoming request: {body}")
    user_input = body.get("text", "")
    if is_triggered(user_input):
        return {
            "type": "message",
            "text": FOLLOW_UP_RESPONSE
        }
    else:
        return {
            "type": "message",
            "text": "No Tableau license request detected."
        }
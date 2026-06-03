import json
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_FILE = os.path.join(BASE_DIR, "output", "events.jsonl")

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def save_event(visitor_id, event_type):

    event = {
        "visitor_id": visitor_id,
        "event_type": event_type,
        "timestamp": datetime.now().isoformat()
    }

    print(event)
    print("Writing to:", OUTPUT_FILE)

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
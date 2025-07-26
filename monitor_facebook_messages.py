import argparse
import os
import time
from typing import List, Dict, Set

import requests


def fetch_messages(page_id: str, access_token: str) -> List[Dict[str, str]]:
    """Fetch messages from a Facebook Page conversations edge."""
    url = f"https://graph.facebook.com/v18.0/{page_id}/conversations"
    params = {
        "access_token": access_token,
        "fields": "messages{message,from,id,created_time}"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    messages: List[Dict[str, str]] = []
    for conv in data.get("data", []):
        for msg in conv.get("messages", {}).get("data", []):
            messages.append(msg)
    return messages


def detect_new_messages(page_id: str, access_token: str, seen_ids: Set[str]) -> List[Dict[str, str]]:
    """Return new messages not present in seen_ids and update seen_ids."""
    messages = fetch_messages(page_id, access_token)
    new = []
    for msg in messages:
        msg_id = msg.get("id")
        if msg_id and msg_id not in seen_ids:
            seen_ids.add(msg_id)
            new.append(msg)
    return new


def monitor(page_id: str, access_token: str, interval: float = 30.0) -> None:
    """Continuously poll Facebook for new messages."""
    seen: Set[str] = set()
    print(f"Monitoring page {page_id} every {interval} seconds... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(interval)
            new = detect_new_messages(page_id, access_token, seen)
            if new:
                print("New messages detected:")
                for msg in new:
                    name = msg.get("from", {}).get("name", "Unknown")
                    created = msg.get("created_time")
                    text = msg.get("message")
                    print(f"[{created}] {name}: {text}")
    except KeyboardInterrupt:
        print("\nStopped monitoring.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor Facebook Marketplace messages")
    parser.add_argument("page_id", help="Facebook Page ID")
    parser.add_argument("access_token", help="Facebook Page access token")
    parser.add_argument("--interval", type=float, default=30.0, help="Polling interval in seconds")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    monitor(args.page_id, args.access_token, args.interval)

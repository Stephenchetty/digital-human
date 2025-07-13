import csv
import os
import time
import argparse
from typing import List, Dict, Set


def load_leads(path: str) -> List[Dict[str, str]]:
    """Load leads from a CSV file."""
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def detect_new_leads(path: str, seen_ids: Set[str]) -> List[Dict[str, str]]:
    """Return new leads not present in seen_ids and update seen_ids."""
    if not os.path.exists(path):
        return []
    leads = load_leads(path)
    new = []
    for lead in leads:
        lead_id = lead.get("id")
        if lead_id and lead_id not in seen_ids:
            seen_ids.add(lead_id)
            new.append(lead)
    return new


def monitor(path: str, interval: float = 30.0) -> None:
    """Continuously monitor the leads file for new entries."""
    seen: Set[str] = set()
    if os.path.exists(path):
        for lead in load_leads(path):
            if "id" in lead:
                seen.add(lead["id"])

    print(f"Monitoring {path} every {interval} seconds... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(interval)
            new = detect_new_leads(path, seen)
            if new:
                print("New leads detected:")
                for lead in new:
                    print("-", lead)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor a CSV file for new business leads")
    parser.add_argument("file", help="Path to the leads CSV file")
    parser.add_argument("--interval", type=float, default=30.0, help="Polling interval in seconds")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    monitor(args.file, args.interval)

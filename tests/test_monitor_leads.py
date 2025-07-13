import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import tempfile
import csv
from monitor_leads import detect_new_leads


def test_detect_new_leads(tmp_path):
    csv_path = tmp_path / "leads.csv"
    # initial leads
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name"])
        writer.writeheader()
        writer.writerow({"id": "1", "name": "Alice"})
    seen = set()
    new = detect_new_leads(str(csv_path), seen)
    assert len(new) == 1
    assert new[0]["name"] == "Alice"

    # add another lead
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name"])
        writer.writerow({"id": "2", "name": "Bob"})
    new = detect_new_leads(str(csv_path), seen)
    assert len(new) == 1
    assert new[0]["name"] == "Bob"

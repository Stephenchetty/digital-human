import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import types
from monitor_facebook_messages import detect_new_messages


def test_detect_new_messages(monkeypatch):
    # Setup a fake fetch_messages function
    messages_sequence = [
        [{"id": "1", "message": "Hello"}],
        [{"id": "1", "message": "Hello"}, {"id": "2", "message": "Hi"}]
    ]
    state = {"idx": 0}

    def fake_fetch_messages(page_id, access_token):
        idx = state["idx"]
        state["idx"] += 1 if state["idx"] < len(messages_sequence) - 1 else 0
        return messages_sequence[idx]

    monkeypatch.setattr("monitor_facebook_messages.fetch_messages", fake_fetch_messages)

    seen = set()
    new = detect_new_messages("page", "token", seen)
    assert len(new) == 1
    assert new[0]["id"] == "1"

    new = detect_new_messages("page", "token", seen)
    assert len(new) == 1
    assert new[0]["id"] == "2"

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import Decision, Event


def write_audit_log(path: str | Path, event: Event, decision: Decision) -> None:
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": event.actor,
        "host": event.host,
        "action": event.action.value,
        "target": event.target,
        "decision": decision.value,
        "metadata": event.metadata,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

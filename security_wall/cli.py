from __future__ import annotations

import argparse
import json
from pathlib import Path

from .logging_utils import write_audit_log
from .models import ActionType, Event
from .policy import evaluate_event, load_policy


def _load_event(path: str | Path) -> Event:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return Event(
        action=ActionType(payload["action"]),
        target=payload["target"],
        actor=payload["actor"],
        host=payload["host"],
        metadata=payload.get("metadata", {}),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Security Wall policy evaluator")
    parser.add_argument("--policy", required=True, help="Path to policy JSON")
    parser.add_argument("--event", required=True, help="Path to event JSON")
    parser.add_argument(
        "--log",
        default="logs/audit.log",
        help="Path to append audit log entries",
    )
    args = parser.parse_args()

    policy = load_policy(args.policy)
    event = _load_event(args.event)
    decision = evaluate_event(policy, event)
    write_audit_log(args.log, event, decision)

    print(
        json.dumps(
            {
                "action": event.action.value,
                "target": event.target,
                "decision": decision.value,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

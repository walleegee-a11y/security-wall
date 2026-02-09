from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import ActionType, Decision, Event, Policy, PolicyRule


def _parse_action(value: str) -> ActionType:
    try:
        return ActionType(value)
    except ValueError as exc:
        raise ValueError(f"Unsupported action type: {value}") from exc


def _parse_decision(value: str) -> Decision:
    try:
        return Decision(value)
    except ValueError as exc:
        raise ValueError(f"Unsupported decision type: {value}") from exc


def load_policy(path: str | Path) -> Policy:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    default_decisions: dict[ActionType, Decision] = {}
    for action_name, decision_name in payload.get("defaults", {}).items():
        default_decisions[_parse_action(action_name)] = _parse_decision(decision_name)

    rules: list[PolicyRule] = []
    for raw_rule in payload.get("rules", []):
        rules.append(
            PolicyRule(
                action=_parse_action(raw_rule["action"]),
                decision=_parse_decision(raw_rule["decision"]),
                targets=list(raw_rule.get("targets", [])),
                note=raw_rule.get("note"),
            )
        )

    return Policy(default_decisions=default_decisions, rules=rules)


def evaluate_event(policy: Policy, event: Event) -> Decision:
    for rule in policy.rules:
        if rule.action != event.action:
            continue
        if _target_matches(rule.targets, event.target):
            return rule.decision

    return policy.default_decisions.get(event.action, Decision.ALLOW)


def _target_matches(targets: Iterable[str], target: str) -> bool:
    if "*" in targets:
        return True
    return target in targets

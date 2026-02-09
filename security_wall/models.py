from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ActionType(str, Enum):
    USB = "usb"
    WEB_UPLOAD = "web_upload"
    APP_EXEC = "app_exec"
    PRINT = "print"
    FILE_BACKUP = "file_backup"
    VULNERABILITY_CHECK = "vuln_check"


class Decision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"


@dataclass(frozen=True)
class PolicyRule:
    action: ActionType
    decision: Decision
    targets: List[str]
    note: Optional[str] = None


@dataclass(frozen=True)
class Policy:
    default_decisions: dict[ActionType, Decision]
    rules: List[PolicyRule]


@dataclass(frozen=True)
class Event:
    action: ActionType
    target: str
    actor: str
    host: str
    metadata: dict[str, str]

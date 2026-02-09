from __future__ import annotations

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")
EVENT_LOG = DATA_DIR / "events.jsonl"
STATUS_FILE = DATA_DIR / "agents.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_agent_status() -> dict[str, Any]:
    if not STATUS_FILE.exists():
        return {"agents": {}}
    return json.loads(STATUS_FILE.read_text(encoding="utf-8"))


def _write_agent_status(payload: dict[str, Any]) -> None:
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_event(event: dict[str, Any]) -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


class SecurityWallHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        response = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self) -> None:  # noqa: N802 - stdlib naming
        if self.path == "/health":
            self._send_json(200, {"status": "ok", "timestamp": _utc_now()})
            return
        if self.path == "/agents":
            self._send_json(200, _load_agent_status())
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802 - stdlib naming
        if self.path not in {"/events", "/agents/heartbeat"}:
            self._send_json(404, {"error": "not_found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_payload = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_payload.decode("utf-8")) if raw_payload else {}
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid_json"})
            return

        if self.path == "/events":
            event = {"received_at": _utc_now(), **payload}
            _append_event(event)
            self._send_json(201, {"status": "recorded", "event": event})
            return

        agent_status = _load_agent_status()
        agent_id = payload.get("agent_id") or "unknown"
        agent_status["agents"][agent_id] = {
            "last_seen": _utc_now(),
            "host": payload.get("host"),
            "ip": payload.get("ip"),
            "version": payload.get("version"),
            "status": payload.get("status", "ok"),
        }
        _write_agent_status(agent_status)
        self._send_json(200, {"status": "updated", "agent_id": agent_id})


def run(host: str = "0.0.0.0", port: int = 9000) -> None:
    server = HTTPServer((host, port), SecurityWallHandler)
    print(f"Security Wall server listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

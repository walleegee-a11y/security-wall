from __future__ import annotations

import json
import time
import urllib.request
from typing import Any


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def send_heartbeat(server_url: str, agent_id: str, host: str, version: str) -> None:
    payload = {
        "agent_id": agent_id,
        "host": host,
        "ip": "127.0.0.1",
        "version": version,
        "status": "ok",
    }
    _post_json(f"{server_url}/agents/heartbeat", payload)


def send_event(server_url: str, event: dict[str, Any]) -> None:
    _post_json(f"{server_url}/events", event)


def main() -> None:
    server_url = "http://127.0.0.1:9000"
    agent_id = "PC-01"
    send_heartbeat(server_url, agent_id, host="PC-01", version="0.1.0")

    sample_event = {
        "agent_id": agent_id,
        "actor": "kim.jiho",
        "action": "usb",
        "target": "KINGSTON_128GB",
        "metadata": {"device_serial": "A1B2C3D4"},
    }
    send_event(server_url, sample_event)

    print("Sent heartbeat and sample event to server.")
    time.sleep(0.2)


if __name__ == "__main__":
    main()

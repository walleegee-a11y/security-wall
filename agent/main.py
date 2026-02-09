from __future__ import annotations

import argparse

from .agent import send_event, send_heartbeat


def main() -> None:
    parser = argparse.ArgumentParser(description="Security Wall agent simulator")
    parser.add_argument("--server", default="http://127.0.0.1:9000", help="Server URL")
    parser.add_argument("--agent-id", default="PC-01", help="Agent identifier")
    parser.add_argument("--host", default="PC-01", help="Host name")
    parser.add_argument("--version", default="0.1.0", help="Agent version")
    parser.add_argument("--action", default="usb", help="Event action")
    parser.add_argument("--target", default="KINGSTON_128GB", help="Event target")
    args = parser.parse_args()

    send_heartbeat(args.server, args.agent_id, host=args.host, version=args.version)
    send_event(
        args.server,
        {
            "agent_id": args.agent_id,
            "actor": "demo.user",
            "action": args.action,
            "target": args.target,
            "metadata": {"source": "agent-sim"},
        },
    )

    print(f"Sent heartbeat and event to {args.server} for {args.agent_id}.")


if __name__ == "__main__":
    main()

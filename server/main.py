from __future__ import annotations

import argparse

from .app import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Security Wall server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=9000, help="Bind port")
    args = parser.parse_args()

    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()

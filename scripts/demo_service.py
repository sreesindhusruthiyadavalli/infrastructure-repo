#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


def check_redis_dependency(redis_host: str = "redis", redis_port: int = 6379, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((redis_host, redis_port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            time.sleep(0.05)
            return True
    except OSError:
        return False


def build_handler(started_at: float, ready_after: float, redis_host: str, redis_port: int):
    class DemoHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            elapsed = time.monotonic() - started_at
            redis_ready = check_redis_dependency(redis_host=redis_host, redis_port=redis_port)

            if self.path == "/live":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"live")
                return

            if self.path == "/ready":
                if elapsed >= ready_after and redis_ready:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"ready")
                else:
                    self.send_response(503)
                    self.end_headers()
                    if elapsed < ready_after:
                        self.wfile.write(b"warming up")
                    else:
                        self.wfile.write(b"redis unavailable")
                return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")

        def log_message(self, format, *args):
            return

    return DemoHandler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo service that is live before it becomes ready")
    parser.add_argument("--host", default="127.0.0.1", help="listen host")
    parser.add_argument("--port", type=int, default=8080, help="listen port")
    parser.add_argument("--ready-after", type=float, default=5.0, help="seconds before /ready returns 200")
    parser.add_argument("--redis-host", default=os.getenv("REDIS_HOST", "redis"), help="hostname of Redis dependency")
    parser.add_argument("--redis-port", type=int, default=int(os.getenv("REDIS_PORT", "6379")), help="TCP port of Redis dependency")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    started_at = time.monotonic()
    server = HTTPServer((args.host, args.port), build_handler(started_at, args.ready_after, args.redis_host, args.redis_port))
    print(
        f"demo service listening on http://{args.host}:{args.port} with /live ready immediately, /ready after {args.ready_after}s and Redis at {args.redis_host}:{args.redis_port}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
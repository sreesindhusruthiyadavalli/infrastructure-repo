#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Callable, Sequence


@dataclass
class CheckResult:
    target: str
    kind: str
    ok: bool
    probe: str = "generic"
    status_code: int | None = None
    latency_ms: float | None = None
    error: str | None = None
    attempts: int = 1


def parse_tcp_target(target: str) -> tuple[str, int]:
    host, separator, port_text = target.rpartition(":")
    if not separator or not host or not port_text.isdigit():
        raise ValueError(f"invalid TCP target '{target}', expected host:port")
    return host, int(port_text)


def check_http_target(target: str, timeout: float) -> CheckResult:
    started = time.perf_counter()
    request = urllib.request.Request(target, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            latency_ms = (time.perf_counter() - started) * 1000
            status_code = response.getcode()
            return CheckResult(
                target=target,
                kind="http",
                ok=200 <= status_code < 400,
                probe="generic",
                status_code=status_code,
                latency_ms=round(latency_ms, 2),
                error=None if 200 <= status_code < 400 else f"unexpected status {status_code}",
            )
    except urllib.error.HTTPError as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        return CheckResult(
            target=target,
            kind="http",
            ok=False,
            probe="generic",
            status_code=exc.code,
            latency_ms=round(latency_ms, 2),
            error=f"unexpected status {exc.code}",
        )
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        return CheckResult(
            target=target,
            kind="http",
            ok=False,
            probe="generic",
            latency_ms=round(latency_ms, 2),
            error=str(exc),
        )


def check_tcp_target(target: str, timeout: float) -> CheckResult:
    host, port = parse_tcp_target(target)
    started = time.perf_counter()

    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency_ms = (time.perf_counter() - started) * 1000
            return CheckResult(
                target=target,
                kind="tcp",
                ok=True,
                probe="generic",
                latency_ms=round(latency_ms, 2),
            )
    except OSError as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        return CheckResult(
            target=target,
            kind="tcp",
            ok=False,
            probe="generic",
            latency_ms=round(latency_ms, 2),
            error=str(exc),
        )


def run_with_retries(
    target: str,
    kind: str,
    probe: str,
    check_fn: Callable[[str, float], CheckResult],
    timeout: float,
    retries: int,
    interval: float,
) -> CheckResult:
    last_result: CheckResult | None = None

    for attempt in range(1, retries + 2):
        result = check_fn(target, timeout)
        result.attempts = attempt
        result.probe = probe
        if result.ok:
            return result
        last_result = result
        if attempt <= retries:
            time.sleep(interval)

    if last_result is None:
        return CheckResult(target=target, kind=kind, probe=probe, ok=False, error="check did not run")

    return last_result


def summarize(results: Sequence[CheckResult]) -> dict[str, object]:
    return {
        "overall_status": "pass" if all(result.ok for result in results) else "fail",
        "checks": [asdict(result) for result in results],
    }


def render_text(results: Sequence[CheckResult]) -> str:
    lines: list[str] = []
    for result in results:
        state = "PASS" if result.ok else "FAIL"
        detail = f"status={result.status_code}" if result.status_code is not None else "status=n/a"
        latency = f"latency_ms={result.latency_ms}" if result.latency_ms is not None else "latency_ms=n/a"
        error = f" error={result.error}" if result.error else ""
        lines.append(
            f"[{state}] kind={result.kind} probe={result.probe} target={result.target} attempts={result.attempts} {detail} {latency}{error}"
        )
    lines.append(f"overall_status={'PASS' if all(result.ok for result in results) else 'FAIL'}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check HTTP and TCP targets for basic service health")
    parser.add_argument("--http", action="append", default=[], help="HTTP/HTTPS target to check")
    parser.add_argument("--tcp", action="append", default=[], help="TCP target in host:port format")
    parser.add_argument("--liveness", action="append", default=[], help="HTTP/HTTPS liveness endpoint to check")
    parser.add_argument("--readiness", action="append", default=[], help="HTTP/HTTPS readiness endpoint to check")
    parser.add_argument("--timeout", type=float, default=2.0, help="timeout in seconds for each attempt")
    parser.add_argument("--retries", type=int, default=0, help="number of retries after the first attempt")
    parser.add_argument("--interval", type=float, default=0.5, help="delay between retries in seconds")
    parser.add_argument("--output", choices=("text", "json"), default="text", help="output format")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.http and not args.tcp and not args.liveness and not args.readiness:
        parser.error("at least one --http, --tcp, --liveness, or --readiness target is required")

    results: list[CheckResult] = []

    for target in args.http:
        results.append(
            run_with_retries(target, "http", "generic", check_http_target, args.timeout, args.retries, args.interval)
        )

    for target in args.tcp:
        results.append(
            run_with_retries(target, "tcp", "generic", check_tcp_target, args.timeout, args.retries, args.interval)
        )

    for target in args.liveness:
        results.append(
            run_with_retries(target, "http", "liveness", check_http_target, args.timeout, args.retries, args.interval)
        )

    for target in args.readiness:
        results.append(
            run_with_retries(target, "http", "readiness", check_http_target, args.timeout, args.retries, args.interval)
        )

    if args.output == "json":
        print(json.dumps(summarize(results), indent=2))
    else:
        print(render_text(results))

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
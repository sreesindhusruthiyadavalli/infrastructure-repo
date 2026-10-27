import importlib.util
import pathlib
import socket
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "health_check.py"
SPEC = importlib.util.spec_from_file_location("health_check", MODULE_PATH)
health_check = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = health_check
SPEC.loader.exec_module(health_check)


class OkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format, *args):
        return


def build_live_not_ready_handler():
    class LiveNotReadyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/live":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"live")
                return

            if self.path == "/ready":
                self.send_response(503)
                self.end_headers()
                self.wfile.write(b"not ready")
                return

            self.send_response(404)
            self.end_headers()

        def log_message(self, format, *args):
            return

    return LiveNotReadyHandler


class HealthCheckTests(unittest.TestCase):
    def test_parse_tcp_target_rejects_bad_format(self):
        with self.assertRaises(ValueError):
            health_check.parse_tcp_target("localhost")

    def test_parse_tcp_target_accepts_host_and_port(self):
        self.assertEqual(health_check.parse_tcp_target("localhost:8080"), ("localhost", 8080))

    def test_summarize_reports_fail_when_any_check_fails(self):
        passing = health_check.CheckResult(target="http://ok", kind="http", ok=True)
        failing = health_check.CheckResult(target="db:5432", kind="tcp", ok=False, error="refused")

        summary = health_check.summarize([passing, failing])

        self.assertEqual(summary["overall_status"], "fail")
        self.assertEqual(len(summary["checks"]), 2)

    def test_check_http_target_passes_for_local_server(self):
        server = HTTPServer(("127.0.0.1", 0), OkHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        try:
            target = f"http://127.0.0.1:{server.server_port}"
            result = health_check.check_http_target(target, timeout=1.0)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

        self.assertTrue(result.ok)
        self.assertEqual(result.status_code, 200)

    def test_check_tcp_target_passes_for_listening_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        host, port = server.getsockname()

        try:
            result = health_check.check_tcp_target(f"{host}:{port}", timeout=1.0)
        finally:
            server.close()

        self.assertTrue(result.ok)

    def test_run_with_retries_marks_probe_type(self):
        result = health_check.run_with_retries(
            "http://example.com/ready",
            "http",
            "readiness",
            lambda target, timeout: health_check.CheckResult(target=target, kind="http", ok=True),
            timeout=1.0,
            retries=0,
            interval=0.0,
        )

        self.assertEqual(result.probe, "readiness")

    def test_tcp_can_pass_while_readiness_fails(self):
        server = HTTPServer(("127.0.0.1", 0), build_live_not_ready_handler())
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        try:
            tcp_result = health_check.check_tcp_target(f"127.0.0.1:{server.server_port}", timeout=1.0)
            ready_result = health_check.run_with_retries(
                f"http://127.0.0.1:{server.server_port}/ready",
                "http",
                "readiness",
                health_check.check_http_target,
                timeout=1.0,
                retries=0,
                interval=0.0,
            )
            live_result = health_check.run_with_retries(
                f"http://127.0.0.1:{server.server_port}/live",
                "http",
                "liveness",
                health_check.check_http_target,
                timeout=1.0,
                retries=0,
                interval=0.0,
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

        self.assertTrue(tcp_result.ok)
        self.assertTrue(live_result.ok)
        self.assertFalse(ready_result.ok)
        self.assertEqual(ready_result.status_code, 503)
        self.assertEqual(live_result.probe, "liveness")
        self.assertEqual(ready_result.probe, "readiness")

    def test_demo_service_redis_dependency_check(self):
        import importlib.util
        import pathlib

        demo_service_path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "demo_service.py"
        spec = importlib.util.spec_from_file_location("demo_service", demo_service_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader is not None
        spec.loader.exec_module(module)

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]

        try:
            accepted = threading.Event()

            def serve_once():
                conn, _ = listener.accept()
                conn.close()
                accepted.set()

            thread = threading.Thread(target=serve_once)
            thread.daemon = True
            thread.start()
            self.assertTrue(module.check_redis_dependency("127.0.0.1", port, timeout=1.0))
            self.assertTrue(accepted.is_set())
        finally:
            listener.close()

        self.assertFalse(module.check_redis_dependency("127.0.0.1", 1, timeout=0.2))


if __name__ == "__main__":
    unittest.main()
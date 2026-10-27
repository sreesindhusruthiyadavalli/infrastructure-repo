# Infrastructure Learning Lab

This repository turns the roadmap in `projectplan.md` into hands-on infrastructure work.

The first lab focuses on a core distributed-systems concern: determining whether a service is reachable and healthy.

## Current lab

- `scripts/health_check.py`: checks TCP, generic HTTP, liveness, and readiness targets with retries and JSON output
- `scripts/demo_service.py`: demo service that is live before it becomes ready, and now also checks Redis dependency readiness
- `scripts/smoke_test_proxy_lab_with_redis.sh`: exercises Redis failure and recovery through the reverse proxy
- `docker-compose.yml`: Compose-managed reverse proxy lab with restart policies, health checks, and Redis dependency ordering
- `proxy-lab/nginx/default.conf`: Nginx TLS reverse proxy for the demo service
- `scripts/generate_local_certs.sh`: creates a local certificate for `demo.internal.test`
- `docs/week-01-distributed-systems-foundations.md`: explains the learning goals and practice exercises for the first step
- `docs/reverse-proxy-tls-lab.md`: DNS, TLS, reverse proxy, and service supervision walkthrough
- `docs/redis-dependency-readiness-lab.md`: Redis dependency-aware readiness, `depends_on`, and liveness vs readiness explanation
- `tests/test_health_check.py`: verifies the health-check behavior locally

## Quick start

Run the test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Check an HTTP endpoint:

```bash
python3 scripts/health_check.py --http https://example.com --output json
```

Check a TCP target:

```bash
python3 scripts/health_check.py --tcp localhost:5432 --retries 2
```

Compare liveness and readiness:

```bash
python3 scripts/demo_service.py --port 8080 --ready-after 10
python3 scripts/health_check.py --tcp 127.0.0.1:8080 --liveness http://127.0.0.1:8080/live --readiness http://127.0.0.1:8080/ready
```

Start the reverse proxy TLS lab:

```bash
./scripts/generate_local_certs.sh
docker compose up -d --build
./scripts/smoke_test_proxy_lab.sh
```

Run the Redis dependency failure and recovery smoke test:

```bash
./scripts/smoke_test_proxy_lab_with_redis.sh
```

## Why start here

Distributed systems depend on health checks for:

- load balancer target selection
- container orchestration probes
- rollout safety
- incident diagnosis
- automated recovery

This is the first building block before moving into Docker, CI/CD, Kubernetes, and observability.
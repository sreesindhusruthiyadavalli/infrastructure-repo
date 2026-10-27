# Week 1 Foundations for Distributed Systems Infrastructure

This is the first practical step from `projectplan.md`.

## Learning goal

Understand how infrastructure determines whether a distributed service is reachable, healthy, and safe to depend on.

## Why this matters

In distributed systems, a service can fail in multiple ways:

- DNS resolves incorrectly
- the host is reachable but the port is closed
- the process accepts a TCP connection but returns failing HTTP responses
- the service responds too slowly for upstream systems to tolerate
- intermittent failures happen during deploys or restarts

Health checks are a core infrastructure primitive because they drive:

- load balancer target registration
- Kubernetes liveness and readiness probes
- automated failover decisions
- deployment gates
- alerting and incident response

## What to learn while using the lab

Focus on these concepts:

1. TCP reachability: can a client open a socket to a host and port?
2. HTTP availability: does the service return a valid response code?
3. Timeouts: how long should infra wait before deciding a dependency is unhealthy?
4. Retries: when is it reasonable to retry instead of failing immediately?
5. Signal quality: how do you avoid checks that are noisy or misleading?

## Lab tool

Use `scripts/health_check.py` to probe TCP targets, generic HTTP endpoints, and explicit liveness/readiness endpoints.

Examples:

```bash
python3 scripts/health_check.py --http https://example.com
python3 scripts/health_check.py --tcp localhost:6379 --retries 2 --interval 1
python3 scripts/health_check.py --liveness http://localhost:8080/live --readiness http://localhost:8080/ready --output json
```

## Liveness vs readiness in this lab

- TCP check: proves only that something is listening on a port
- Liveness check: proves the process is up enough to answer a basic endpoint such as `/live`
- Readiness check: proves the instance is safe to receive traffic now, often via `/ready`

These are not interchangeable.

A service can be:

- TCP reachable but not ready
- live but not ready
- live and ready

That difference is common during startup, dependency outages, migrations, and cache warmup.

## Demo: port open, liveness passes, readiness fails

Run the demo service:

```bash
python3 scripts/demo_service.py --port 8080 --ready-after 10
```

While it is warming up, run:

```bash
python3 scripts/health_check.py --tcp 127.0.0.1:8080 --liveness http://127.0.0.1:8080/live --readiness http://127.0.0.1:8080/ready
```

Expected behavior during warmup:

- TCP passes because the port is open
- liveness passes because the process is running
- readiness fails with `503` because the app is not ready for traffic yet

After the `--ready-after` window expires, run the same command again and readiness should pass too.

## Exercises

1. Run one successful HTTP check and one failing TCP check. Compare the output and exit codes.
2. Start a local service, then stop it, and observe how the check result changes.
3. Increase `--timeout` and `--retries` while the demo service approaches readiness. Notice that retries only help if the service becomes ready before the retry budget is exhausted.
4. Compare `--liveness http://localhost:8080/live` and `--readiness http://localhost:8080/ready`. The first asks whether the process is alive; the second asks whether it is safe to send traffic.
5. Use the demo service during warmup and observe that TCP success is a bad readiness signal because the port is open even though `/ready` still returns `503`.

## How this connects to the roadmap

This lab prepares you for the next layers in the plan:

- Docker health checks
- Compose service dependency checks
- Kubernetes probes
- CI smoke tests
- post-deploy verification
- alerting and incident runbooks

## Next build step

The next lab is now available in [docs/reverse-proxy-tls-lab.md](docs/reverse-proxy-tls-lab.md). It puts Nginx in front of the demo service with TLS so you can practice DNS, HTTP redirects, certificates, and service supervision together.
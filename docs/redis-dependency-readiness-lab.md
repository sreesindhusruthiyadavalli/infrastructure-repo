# Redis Dependency-Aware Readiness Lab

This lab turns the live-vs-ready learning into a more realistic distributed-systems pattern.

The service process may still be alive while it cannot serve traffic because it depends on Redis. That is the difference between liveness and readiness in practice.

## What you will learn

1. What `depends_on` does in Compose
2. What `condition: service_healthy` means
3. The difference between liveness and readiness probes
4. How a service can be alive but still not ready
5. How to exercise a real failure and recovery cycle with Redis

## Files involved in this Redis dependency lab

- `docker-compose.yml`: defines the Redis service and the `depends_on` startup dependency
- `scripts/demo_service.py`: checks whether Redis is reachable and changes `/ready` based on that
- `scripts/smoke_test_proxy_lab_with_redis.sh`: exercise the failure/recovery loop end-to-end
- `tests/test_health_check.py`: verifies the dependency check and live-vs-ready behavior locally
- `docs/reverse-proxy-tls-lab.md`: the earlier reverse proxy and TLS context for the lab setup

## Why Redis makes this interesting

A service can be running but not usable if it depends on a backing store such as Redis.

That is the usual production pattern:

- the process is alive
- the dependency is not reachable
- therefore the service is not ready to serve traffic

This is why checking only a port or process state is not enough.

## Code behavior in the demo service

The demo service in `scripts/demo_service.py` implements two endpoints:

- `/live`: returns `200` if the process is alive
- `/ready`: returns `200` only when:
  - the startup wait window is complete, and
  - Redis is reachable

If Redis is unavailable, `/ready` returns `503` even though `/live` still works.

That maps directly to the distributed-systems idea:

- liveness = is the process alive?
- readiness = is it ready to handle real work?

## `depends_on` and `condition: service_healthy`

In `docker-compose.yml`, the app service is configured like this:

```yaml
depends_on:
  redis:
    condition: service_healthy
```

This means:

- start the Redis container
- wait until its healthcheck passes
- then start the dependent service

This is a startup ordering rule.

It is not the same as the runtime readiness of the application itself.

### What is `service_healthy`?

It means the dependency has passed its healthcheck. In this repo, Redis uses:

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 2s
  retries: 5
  start_period: 2s
```

If `redis-cli ping` succeeds, Redis is marked healthy.

### `service_started` vs `service_healthy`

The common Compose conditions are:

- `service_started`: start after the dependency container has started
- `service_healthy`: start after the dependency has passed its healthcheck

This is a startup concern, not a runtime request-serving concern.

## LivenessProbe vs ReadinessProbe

This is the same idea in orchestrators such as Kubernetes.

### LivenessProbe

This checks whether the process is still alive.

Typical meaning:

- if the process is dead, restart it
- if it is alive, keep it running

This is not a proof that the service is usable yet.

### ReadinessProbe

This checks whether the service is ready to receive traffic.

Typical meaning:

- it may not be ready while warming up
- it may not be ready while a dependency is down
- traffic should be routed away from it until it is ready

### In plain language

- liveness: “is the app still running?”
- readiness: “can this app serve real work right now?”

A service can be live but not ready.

That is exactly what this Redis lab demonstrates.

## Step-by-step exercise

Run the stack:

```bash
cd /Users/sryadava/Documents/Sruthi/Python/infrastructure-repo
docker compose up -d --build
```

Check the endpoints:

```bash
curl -sS -i --resolve 'demo.internal.test:8443:127.0.0.1' --insecure 'https://demo.internal.test:8443/live'
curl -sS -i --resolve 'demo.internal.test:8443:127.0.0.1' --insecure 'https://demo.internal.test:8443/ready'
```

Expected result:

- `/live` returns `200`
- `/ready` returns `200` once Redis is healthy and the warmup passes

### Failure mode

Stop Redis:

```bash
docker compose stop redis
```

Then check:

```bash
curl -sS -i --resolve 'demo.internal.test:8443:127.0.0.1' --insecure 'https://demo.internal.test:8443/live'
curl -sS -i --resolve 'demo.internal.test:8443:127.0.0.1' --insecure 'https://demo.internal.test:8443/ready'
```

Expected result:

- `/live` still returns `200`
- `/ready` returns `503 Service Unavailable`

That is the key learning moment.

It proves the service is alive but not ready.

### Recovery

Start Redis again:

```bash
docker compose start redis
```

Check readiness again:

```bash
curl -sS -i --resolve 'demo.internal.test:8443:127.0.0.1' --insecure 'https://demo.internal.test:8443/ready'
```

Expected result:

- `/ready` returns `200`

That demonstrates recovery: the dependency is back and readiness is restored.

## Smoke test script for this lab

We added a dedicated script:

- `scripts/smoke_test_proxy_lab_with_redis.sh`

It runs the failure/recovery exercise automatically.

Usage:

```bash
./scripts/smoke_test_proxy_lab_with_redis.sh
```

This script intentionally shows the exact lifecycle we want to teach:

1. baseline liveness and readiness
2. Redis shutdown
3. readiness failure while liveness remains healthy
4. Redis restart
5. readiness recovery

## The big lesson

This is the heart of distributed systems reliability:

- startup ordering helps avoid boot races
- health checks make dependency readiness visible
- runtime probes tell us whether the service should receive traffic
- a dependency outage can make a service live but not ready

That is the difference between a process that is running and a service that is actually safe to route traffic to.

## Practice prompts

1. Change the warmup time in `docker-compose.yml` and observe the readiness delay.
2. Stop Redis and see whether `/live` remains `200` while `/ready` fails.
3. Compare `depends_on` startup behavior with runtime `/ready` behavior.
4. Explain the difference between Compose startup gating and Kubernetes readiness checks.
5. Write down the sequence of events: startup -> dependency healthy -> ready -> dependency fails -> not ready -> dependency recovers -> ready again.

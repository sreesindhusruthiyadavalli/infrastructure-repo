# Reverse Proxy TLS Lab

This lab puts Nginx in front of the demo service so you can practice local DNS, HTTP redirects, TLS certificates, and service supervision together.

## What you will learn

1. DNS: map a local hostname to `127.0.0.1`
2. HTTP: understand the redirect from plain HTTP to HTTPS
3. Certificates: generate and inspect a self-signed certificate with SANs
4. Reverse proxying: route client traffic through Nginx to the demo service
5. Service supervision: use Compose health checks, restart policies, and logs

## Lab layout

- `docker-compose.yml`: runs the demo service and reverse proxy together
- `docker/demo-service.Dockerfile`: container image for the demo service
- `proxy-lab/nginx/default.conf.template`: Nginx reverse proxy and TLS config template
- `proxy-lab/nginx/40-configure-resolver.sh`: startup hook that reads the container DNS server from `/etc/resolv.conf`
- `scripts/generate_local_certs.sh`: generates a local self-signed certificate
- `scripts/smoke_test_proxy_lab.sh`: checks redirect, liveness, and readiness through the proxy

## How runtime DNS resolution works

The reverse proxy does not hardcode the Podman network DNS server.

Instead, it discovers that DNS server at container startup and writes the final Nginx config from a template.

The flow is:

1. Podman starts the `reverse-proxy` container and writes `/etc/resolv.conf` inside it.
2. The startup hook `proxy-lab/nginx/40-configure-resolver.sh` reads the first `nameserver` entry from `/etc/resolv.conf`.
3. That script replaces the placeholder in `proxy-lab/nginx/default.conf.template` and writes the real config to `/etc/nginx/conf.d/default.conf`.
4. Nginx starts with a `resolver` directive that matches the current container network DNS server.
5. When `proxy_pass` needs to resolve `demo-service`, Nginx uses that runtime-derived resolver.

This matters because the backend container can be recreated with a different IP address. The DNS server remains the stable way to find the current `demo-service` address.

### Files involved

- `docker/reverse-proxy.Dockerfile`: packages the template and startup hook into the proxy image
- `proxy-lab/nginx/default.conf.template`: contains the placeholder `__CONTAINER_DNS_RESOLVER__`
- `proxy-lab/nginx/40-configure-resolver.sh`: reads `/etc/resolv.conf` and renders the final config
- `/etc/nginx/conf.d/default.conf`: generated at container startup and used by Nginx

### Verify it yourself

Check the container nameserver:

```bash
podman exec infra-reverse-proxy cat /etc/resolv.conf
```

Check the active Nginx resolver:

```bash
podman exec infra-reverse-proxy nginx -T 2>&1 | grep resolver
```

The IP in the `resolver` line should match the `nameserver` value from `/etc/resolv.conf`.

## Setup

Generate a local certificate:

```bash
./scripts/generate_local_certs.sh
```

Add a local DNS entry:

```text
127.0.0.1 demo.internal.test
```

On macOS, that means adding the line to `/etc/hosts`.

Start the lab:

```bash
docker compose up -d --build
```

At startup, the reverse-proxy container reads its own `/etc/resolv.conf`, extracts the current Podman network nameserver, and renders the Nginx `resolver` directive from that runtime value.

Check container health and supervision state:

```bash
docker compose ps
docker compose logs reverse-proxy
docker compose logs demo-service
```

## What to observe

### HTTP redirect

```bash
curl -I --resolve demo.internal.test:8081:127.0.0.1 http://demo.internal.test:8081/live
```

You should see a redirect to `https://demo.internal.test:8443/live`.

### HTTPS through the reverse proxy

```bash
curl --resolve demo.internal.test:8443:127.0.0.1 --insecure https://demo.internal.test:8443/live
```

This reaches the proxy over TLS and then the demo service over the internal service network.

### Readiness during warmup

Immediately after startup:

```bash
curl -i --resolve demo.internal.test:8443:127.0.0.1 --insecure https://demo.internal.test:8443/ready
```

Expected behavior:

- the container port is open
- `/live` returns `200`
- `/ready` returns `503` until the warmup window expires

That is the same distributed-systems distinction you practiced earlier, but now it is happening through a real reverse proxy and TLS endpoint.

## Practice exercises

1. Run `openssl x509 -in proxy-lab/certs/demo.internal.test.crt -text -noout` and inspect the SAN entries.
2. Remove the hosts entry temporarily and observe the DNS failure mode.
3. Run `docker compose restart demo-service` and watch how `/live` and `/ready` change during recovery.
4. Change `READY_AFTER` in `docker-compose.yml` and see how it affects readiness timing.
5. Run `podman exec infra-reverse-proxy cat /etc/resolv.conf` and compare that nameserver to the rendered config from `podman exec infra-reverse-proxy nginx -T`.

## Cleanup

```bash
docker compose down
```
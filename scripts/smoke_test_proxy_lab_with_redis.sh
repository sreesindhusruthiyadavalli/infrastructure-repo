#!/usr/bin/env bash

set -euo pipefail

host_name="demo.internal.test"
https_url="https://${host_name}:8443"

printf '\n=== baseline checks ===\n'
printf 'live: '
curl -sS -i --resolve "${host_name}:8443:127.0.0.1" --insecure "${https_url}/live" | head -n 20
printf '\nready: '\ncurl -sS -i --resolve "${host_name}:8443:127.0.0.1" --insecure "${https_url}/ready" | head -n 20

printf '\n=== stopping redis ===\n'
docker compose stop redis

printf '\n=== ready while redis is down ===\n'
curl -sS -i --resolve "${host_name}:8443:127.0.0.1" --insecure "${https_url}/ready" | head -n 20

printf '\n=== live while redis is down ===\n'
curl -sS -i --resolve "${host_name}:8443:127.0.0.1" --insecure "${https_url}/live" | head -n 20

printf '\n=== starting redis ===\n'
docker compose start redis

printf '\n=== ready after redis comes back ===\n'
curl -sS -i --resolve "${host_name}:8443:127.0.0.1" --insecure "${https_url}/ready" | head -n 20

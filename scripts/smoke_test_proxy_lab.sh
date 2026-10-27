#!/usr/bin/env bash

set -euo pipefail

host_name="demo.internal.test"

echo "checking HTTP redirect"
curl -sS -I --resolve "$host_name:8081:127.0.0.1" "http://$host_name:8081/live"

echo "checking HTTPS liveness"
curl -sS --resolve "$host_name:8443:127.0.0.1" --insecure "https://$host_name:8443/live"

echo "checking HTTPS readiness"
curl -sS -i --resolve "$host_name:8443:127.0.0.1" --insecure "https://$host_name:8443/ready"
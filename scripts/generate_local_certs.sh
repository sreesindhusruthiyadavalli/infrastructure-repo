#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cert_dir="$repo_root/proxy-lab/certs"
host_name="demo.internal.test"
key_file="$cert_dir/$host_name.key"
cert_file="$cert_dir/$host_name.crt"

mkdir -p "$cert_dir"

openssl req \
  -x509 \
  -nodes \
  -days 30 \
  -newkey rsa:2048 \
  -keyout "$key_file" \
  -out "$cert_file" \
  -subj "/CN=$host_name" \
  -addext "subjectAltName=DNS:$host_name,DNS:localhost,IP:127.0.0.1"

echo "generated $cert_file and $key_file"
echo "add this hosts entry if needed: 127.0.0.1 $host_name"
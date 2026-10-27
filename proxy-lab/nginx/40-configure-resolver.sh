#!/bin/sh

set -eu

resolver_ip="$(awk '/^nameserver / { print $2; exit }' /etc/resolv.conf)"

if [ -z "$resolver_ip" ]; then
    echo "failed to determine container DNS resolver from /etc/resolv.conf" >&2
    exit 1
fi

sed "s/__CONTAINER_DNS_RESOLVER__/$resolver_ip/g" \
    /opt/nginx/default.conf.template \
    > /etc/nginx/conf.d/default.conf

echo "using container DNS resolver: $resolver_ip"
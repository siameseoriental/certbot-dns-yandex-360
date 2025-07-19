#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

certbot certonly \
            --authenticator dns-yandex-360 \
            --domains "*.example.com" \
            --dns-yandex-360-credentials /path/to/yandex/config.ini \
            --non-interactive \
            --agree-tos \
            --force-renewal \
            --verbose

# Reload web-server service. For NGINX:
nginx -t && service nginx reload
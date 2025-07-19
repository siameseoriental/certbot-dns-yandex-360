# Certbot DNS Plugin for Yandex 360
# Let's Encrypt плагин для автоматизации создания wildcard сертификата на DNS Яндекс 360

This plugin automates the process of creation wildcard certificates for domain by completing a `dns-01` challenge by creating and managing DNS records using the Yandex API 360.

## Requirements

- Python 3.6+
- Certbot 1.1.0 or newer
- Access to [Yandex API 360](https://yandex.ru/dev/api360/doc/ru/access) credentials 

## Installation and usage

### Install the Plugin

Clone this repository or download the source code to your system, then run the following command at the root of the source directory:

```shell
pip install .
```
### Check plugin installation

```shell
sudo certbot --verbose plugins
```

### Create config.ini file

```shell
touch config.ini
```
```ini
[API]
endpoint=YOUR_YANDEX_360_API_ENDPOINT
token=YOUR_YANDEX_360_API_TOKEN
```
### Execute certbot in test mode

```shell
sudo certbot certonly \
            --authenticator dns-yandex-360 \
            --domains "*.example.com" \
            --dry-run \
            --verbose
```

### Execute certbot in production mode

```shell
sudo certbot certonly \
            --authenticator dns-yandex-360 \
            --domains "*.example.com" \
            --dns-yandex-360-credentials /path/to/yandex/config.ini \
            --non-interactive \
            --agree-tos \
            --force-renewal \
            --verbose
```
Reload web-server service. For NGINX:
```shell
sudo service nginx reload
```

### Renew wildcard certificate

To automate the process of renewal use provided script `wildcard_cert_renewal.sh`

```shell
sudo chmod +x wildcard_cert_renewal.sh
sudo ./wildcard_cert_renewal.sh
```

Or create a root cron job to execute script monthly
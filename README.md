# Bundlewrap configuration for [MikroTik Prometheus Exporter](https://github.com/akpw/mktxp)

This bundle installs and configure https://github.com/akpw/mktxp as a sytemd-Service.

It will automatically add your RouterOS Devices, if you defined `mikrotik_exporter` metadata on your RouterOS Device
the bundle will use the information from the first `routeros_board` entry.

# Configuration
See `defaults` in `metadata.py`

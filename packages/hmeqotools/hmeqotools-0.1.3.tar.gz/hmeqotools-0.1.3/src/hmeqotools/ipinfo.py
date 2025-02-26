from __future__ import annotations

import os
import socket
import sys
from collections import defaultdict
from typing import Any

import httpx


def get_local_ip() -> str:
    """Get local IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except socket.error:
        return socket.gethostbyname(socket.gethostname())


if sys.platform == "win32":

    def get_local_ip2() -> tuple[str, str]:
        """Get local IP address, return (ipv4, ipv6)."""
        output = [line for line in os.popen("ipconfig")]
        ipv4 = ""
        ipv6 = ""
        for i, line in enumerate(output):
            if "IPv4" in line and output[i + 2][-2] != " ":
                ipv4 = line[line.find(":") + 2:-1]
            elif "IPv6" in line and output[i + 3][-2] != " ":
                ipv6 = line[line.find(":") + 2:-1]
        return ipv4, ipv6


def get_public_ip() -> str:
    """Get public IP address.

    Return the public IP address if it is available, otherwise return 127.0.0.1.
    """
    try:
        return httpx.get("https://api.ipify.org").text
    except httpx.RequestError:
        return "127.0.0.1"


def get_public_ip_json() -> dict[str, Any]:
    """Get public IP address as JSON."""
    try:
        return httpx.get("https://ipinfo.io/json").json()
    except httpx.RequestError:
        return defaultdict(str, {"ip": "127.0.0.1"})


def get_ip_info(ip: str) -> dict[str, Any]:
    """Retrieves the information about the IP address."""
    url = f"https://freegeoip.app/json/{ip}"
    headers = {"accept": "application/json", "content-type": "application/json"}
    try:
        return httpx.get(url, headers=headers).json()
    except httpx.RequestError:
        return defaultdict(str, {"ip": "127.0.0.1"})

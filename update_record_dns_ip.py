#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_ip() -> str:
    """Fetch external IP address."""
    response = requests.get("https://api.ipify.org/")
    return response.text.strip()

def has_ip_changed(current_ip: str) -> bool:
    """Check if IP has changed since last time."""
    try:
        with open("last_ip.txt", "r") as file:
            last_ip = file.read().strip()
            return last_ip != current_ip
    except FileNotFoundError:
        return True  # File doesn't exist, assume IP has changed

def update_dns_records(ip_address: str, records: dict):
    """Update DNS records via Cloudflare API."""
    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    email = os.getenv("CLOUDFLARE_EMAIL")
    api_key = os.getenv("CLOUDFLARE_GLOBAL_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": email,
        "X-Auth-Key": api_key
    }

    endpoint_template = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}"

    for dns_record_id, name in records.items():
        data = {
            "content": ip_address,
            "name": name,
            "proxied": True,
            "type": "A",
            "ttl": 3600
        }

        response = requests.put(endpoint_template.format(zone_id=zone_id, dns_record_id=dns_record_id), headers=headers, json=data)
        if response.status_code == 200:
            print(f"Updated IP address for record {dns_record_id} ({name}) to {ip_address}")
        else:
            print(f"Failed to update IP address for record {dns_record_id} ({name}). Response: {response.text}")

def main():
    current_ip = get_ip()
    if has_ip_changed(current_ip):
        # Dictionary of DNS record IDs and their associated names
        records = {
            "id 1": "domain name 1",
            "id 2": "domain name 2"
        }
        update_dns_records(current_ip, records)
        with open("last_ip.txt", "w") as file:
            file.write(current_ip)
    else:
        print("IP address hasn't changed since last check. Exiting...")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Fetch external IP address
response = requests.get("https://api.ipify.org/")
ip_address = response.text.strip()

# Check if IP has changed since last time
try:
    with open("last_ip.txt", "r") as file:
        last_ip = file.read().strip()
        if last_ip == ip_address:
            print("IP address hasn't changed since last check. Exiting...")
            exit()
except FileNotFoundError:
    pass  # If the file doesn't exist, continue to update the DNS record

# Current date and time comment
comment = datetime.now().strftime('%Y-%m-%d %H:%M')

# Cloudflare API details
endpoint = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}"

zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
email = os.getenv("CLOUDFLARE_EMAIL")
api_key = os.getenv("CLOUDFLARE_GLOBAL_API_KEY")

# Dictionary of DNS record IDs and their associated names
records = {
    "cloudflare-record-id1": "domain.com",
    "cloudflare-record-id2": "sub.domain1",
    "cloudflare-record-id3": "sub.domain2"
}

headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": email,
    "X-Auth-Key": api_key
}

# Iterate through each DNS record ID and name, and update them
for dns_record_id, name in records.items():
    data = {
        "content": ip_address,
        "name": name,
        "proxied": True,
        "type": "A",
        "comment": comment,
        "tags": [],
        "ttl": 3600
    }

    response = requests.put(endpoint.format(zone_id=zone_id, dns_record_id=dns_record_id), headers=headers, json=data)
    if response.status_code == 200:
        print(f"Updated IP address for record {dns_record_id} ({name}) to {ip_address}")
        with open("last_ip.txt", "w") as file:
            file.write(ip_address)
    else:
        print(f"Failed to update IP address for record {dns_record_id} ({name}). Response: {response.text}")

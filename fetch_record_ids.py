#!/usr/bin/env python3

import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Cloudflare API endpoint
endpoint = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

# Get Cloudflare details from environment variables
zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
email = os.getenv("CLOUDFLARE_EMAIL")
api_key = os.getenv("CLOUDFLARE_GLOBAL_API_KEY")
record_name = os.getenv("DOMAIN_NAME")

# Print out the values of environment variables for debugging
print(f"CLOUDFLARE_ZONE_ID: {zone_id}")
print(f"CLOUDFLARE_EMAIL: {email}")
print(f"DOMAIN_NAME: {record_name}")

# Ensure API key is set and print a masked version for debugging
if api_key:
    print(f"CLOUDFLARE_GLOBAL_API_KEY: {'*' * (len(api_key) - 4) + api_key[-4:]}")
else:
    print("CLOUDFLARE_GLOBAL_API_KEY: Not set")

# Check if all necessary environment variables are set
if not all([zone_id, email, api_key, record_name]):
    raise EnvironmentError("Please ensure all required environment variables are set: "
                           "CLOUDFLARE_ZONE_ID, CLOUDFLARE_EMAIL, CLOUDFLARE_GLOBAL_API_KEY, DOMAIN_NAME")

headers = {
    "X-Auth-Email": email,
    "X-Auth-Key": api_key,
    "Content-Type": "application/json"
}

response = requests.get(endpoint.format(zone_id=zone_id), headers=headers)
data = response.json()

# Print the full API response for debugging
print(f"API Response: {data}")

# Check if the API call was successful
if not response.ok:
    raise Exception(f"Error fetching data from Cloudflare API: {data.get('errors', data)}")

# Convert the 'result' key values into a pandas DataFrame
df = pd.DataFrame(data['result'])

# Ensure the directory exists
os.makedirs("data", exist_ok=True)

# Export the DataFrame to a CSV file with column names
df.to_csv(f"data/cloudflare_{record_name}_data.csv", index=False)

# Find and print the recordID for the specified record
filtered_df = df[df['name'] == record_name]
if not filtered_df.empty:
    record_id = filtered_df['id'].values[0]
    print(f"The recordID for {record_name} is: {record_id}")
else:
    print(f"No records found for {record_name}")

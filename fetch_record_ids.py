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

headers = {
    "X-Auth-Email": email,
    "X-Auth-Key": api_key,
    "Content-Type": "application/json"
}

response = requests.get(endpoint.format(zone_id=zone_id), headers=headers)
data = response.json()

# Convert the 'result' key values into a pandas DataFrame
df = pd.DataFrame(data['result'])

# Export the DataFrame to a CSV file with column names
df.to_csv("data/cloudflare_"+ record_name +"_data.csv", index=False)

# Find and print the recordID for the specified record
"""filtered_df = df[df['name'] == record_name]
if not filtered_df.empty:
    record_id = filtered_df['id'].values[0]
    print(f"The recordID for {record_name} is: {record_id}")
else:
    print(f"No records found for {record_name}")
"""
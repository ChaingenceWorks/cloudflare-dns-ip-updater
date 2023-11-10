# CLOUDFLARE DNS IP UPDATER

#### Chaingence

[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![Python 3](https://img.shields.io/badge/python-yellow.svg)](https://www.python.org/downloads/)
[![Cloudflare](https://img.shields.io/badge/cloudflare-red.svg)](https://www.cloudflare.com/)
[![Cloudflare API](https://img.shields.io/badge/cloudflare-api-red.svg)](https://developers.cloudflare.com/api/)


## Requirements

* python==3.9+

## Install virtualenv
pip install virtualenv

### Creating a Virtual Environment
python3 -m venv myenv

### Activating the Virtual Environment
- On Windows:
```
myenv\Scripts\activate
```
- On macOS and Linux:
```
source myenv/bin/activate
```

### Deactivating the Virtual Environment
```
deactivate
```

## Setup and auto installation

For this purpose you use following commands:

```
pip install --upgrade pip
pip install -r requirements.txt
```

# Setup and manual installation
```
pip install --upgrade pip
pip install datetime
pip install os
pip install requests
pip install python-dotenv
```

# Preparation
## Setup .env
Rename the env -> .env file and add Cloudflare information to .env file:
- CLOUDFLARE_ZONE_ID="your_cloudflare_zone_id"
- CLOUDFLARE_EMAIL="your_cloudflare_email_address"
- CLOUDFLARE_GLOBAL_API_KEY="your_cloudflare_global_api_key"
- DOMAIN_NAME="your_domain_name"

## Fetch record ids from Cloudflare:
Execute the `fetch_record_ids.py` script to get the record ids and names.

# Execution
## Manual Execution:
### Update the record IPs for Cloudflare DNS:
Add the record ids and names to the dictionary records = {} and execute the `update_record_dns_ip.py` script to update the IPs in the DNS records in Cloudflare.

## Auto Execution:
### 1. Preparation
1. Update the path in the `run_python.sh` Bash script.
2. Make the Bash script executable:
Provide execute permissions to the Bash script:
```
chmod +x /usr/local/bin/run_python.sh
```

### 2. Setup cronjob
```
*/1 * * * * /usr/local/bin/run_python.sh
@reboot /usr/local/bin/run_python.sh >> /var/log/run_python.log
```

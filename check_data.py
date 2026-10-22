import requests
import base64
import json

WP_URL = "http://city-service-generator.local/wp-json/wp/v2/pages/"
WP_USER = "shrijalkothadiya@gmail.com"
WP_APP_PASSWORD = "zuMv 7mII m4Ov 4vzV nEWp WvFt" 
# PUT THE PAGE ID OF THE BROKEN MUMBAI PAGE HERE
PAGE_ID = "13" # Change this if your Mumbai page has a different ID

auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
headers = {"Authorization": f"Basic {token}"}

response = requests.get(f"{WP_URL}{PAGE_ID}?context=edit", headers=headers)
data = response.json()

print("--- META DATA ---")
# This will print all custom fields the plugin is using!
print(json.dumps(data.get("meta", {}), indent=2))
import requests
import base64

WP_URL = "http://city-service-generator.local/wp-json/wp/v2/pages/"
WP_USER = "shrijalkothadiya@gmail.com"
WP_APP_PASSWORD = "zuMv 7mII m4Ov 4vzV nEWp WvFt" 
PAGE_ID = "13" # Put your Mumbai Plumber page ID here

auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
headers = {"Authorization": f"Basic {token}"}

# Fetch the page and print the excerpt
response = requests.get(f"{WP_URL}{PAGE_ID}", headers=headers)
data = response.json()

print("--- EXCERPT SAVED IN DATABASE ---")
print(data.get("excerpt", {}).get("raw", "No excerpt found."))
import requests
import base64

WP_URL = "http://city-service-generator.local/wp-json/wp/v2/pages/"
WP_USER = "shrijalkothadiya@gmail.com"
WP_APP_PASSWORD = "zuMv 7mII m4Ov 4vzV nEWp WvFt" 

# Replace with the ID of your broken Mumbai page. 
# (If you don't know it, just run it, it will ask you to find the page ID).
PAGE_ID = "13" 

auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

# Reset content to just the shortcode
update_data = {"content": "[local_service_website]"}
response = requests.post(f"{WP_URL}{PAGE_ID}", json=update_data, headers=headers)

if response.status_code == 200:
    print("SUCCESS! The page layout has been repaired and reset to the shortcode.")
else:
    print(f"Error: {response.status_code}")
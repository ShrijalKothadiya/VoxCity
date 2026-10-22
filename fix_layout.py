import requests
import base64

WP_URL = "http://city-service-generator.local/wp-json/wp/v2/pages/"
WP_USER = "shrijalkothadiya@gmail.com"
WP_APP_PASSWORD = "zuMv 7mII m4Ov 4vzV nEWp WvFt" 

# FIND THE PAGE ID OF YOUR MUMBAI PLUMBER PAGE
# Look at the URL when you edit the page: post.php?post=13&action=edit -> ID is 13
PAGE_ID = "13" 

auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

# Force the content to be EXACTLY just the shortcode
update_data = {"content": "[local_service_website]"}
response = requests.post(f"{WP_URL}{PAGE_ID}", json=update_data, headers=headers)

if response.status_code == 200:
    print("SUCCESS! The page layout has been reset. Refresh your WordPress page and it should be fixed.")
else:
    print(f"Error: {response.status_code} - {response.text}")
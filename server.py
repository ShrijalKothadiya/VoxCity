import os
import uuid
import requests
import base64
import re
from mcp.server import MCPServer

# --- SECURE CONFIGURATION ---
# This reads from the cloud server environment. 
# The second value is the fallback for your local testing.
WP_BASE_URL = os.environ.get("WP_BASE_URL", "http://city-service-generator.local")
WP_USER = os.environ.get("WP_USER", "shrijalkothadiya@gmail.com")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "zuMv 7mII m4Ov 4vzV nEWp WvFt")

# Construct the URLs dynamically
WP_URL = f"{WP_BASE_URL}/wp-json/wp/v2/"
CUSTOM_API_URL = f"{WP_BASE_URL}/wp-json/voice-agent/v1/message"

mcp = MCPServer("CityServiceVoiceAgent")

pending_drafts = {}

def get_headers():
    auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
    token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

@mcp.tool()
def find_and_draft_update(city: str, service: str, custom_message: str) -> str:
    search_query = f"{city} {service}"
    response = requests.get(f"{WP_URL}search?search={search_query}&per_page=5", headers=get_headers())
    
    if response.status_code != 200:
        return f"Error searching WordPress: {response.status_code}"
        
    results = response.json()
    valid_pages = [r for r in results if r['subtype'] == 'page']
    
    if not valid_pages:
        return f"I could not find a published page for '{city} {service}'. Please generate and publish it first."
        
    page_id = str(valid_pages[0]['id'])
    page_title = valid_pages[0]['title'].replace("&#8211;", "-").replace("&amp;", "&")
    
    draft_id = str(uuid.uuid4())[:8] 
    pending_drafts[draft_id] = {
        "page_id": page_id, 
        "custom_message": custom_message,
        "page_title": page_title
    }
    
    return f"I found the page '{page_title}'. I have drafted a new banner: '⚠️ {custom_message}'. Draft ID is {draft_id}. Please confirm to publish."

@mcp.tool()
def confirm_and_publish(draft_id: str) -> str:
    if draft_id not in pending_drafts:
        return f"Error: Draft ID {draft_id} not found."
        
    draft = pending_drafts.pop(draft_id)
    page_id = draft["page_id"]
    custom_message = draft["custom_message"]
    
    try:
        # We send the message to our custom WordPress endpoint
        payload = {
            "page_id": page_id,
            "message": custom_message
        }
        
        update_response = requests.post(CUSTOM_API_URL, json=payload)
        
        if update_response.status_code == 200:
            return f"Success! The banner has been successfully injected into the live page."
        else:
            return f"WordPress Error: {update_response.status_code} - {update_response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    mcp.settings.port = port
    mcp.settings.host = "0.0.0.0"
    mcp.run(transport="streamable-http")

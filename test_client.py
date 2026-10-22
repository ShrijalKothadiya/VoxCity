import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import re

async def run_test():
    url = "http://127.0.0.1:8000/mcp"
    print("Connecting to the voice agent...\n")
    
    async with streamable_http_client(url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # 1. Draft a change
            page_id = "2" # Your Sample Page ID
            print(f"👤 User (voice): 'Change the opening time on page {page_id} to 11 a.m.'")
            res_draft = await session.call_tool("draft_page_update", arguments={"page_id": page_id, "new_opening_time": "11:00 AM"})
            print(f"🤖 Agent: {res_draft.content[0].text}\n")
            
            # 2. Confirm the change
            match = re.search(r'Draft ID is ([a-zA-Z0-9-]+)', res_draft.content[0].text)
            if match:
                draft_id = match.group(1)
                print("👤 User (voice): 'Yes, confirm and publish it.'")
                res_confirm = await session.call_tool("confirm_and_publish", arguments={"draft_id": draft_id})
                print(f"🤖 Agent: {res_confirm.content[0].text}\n")

if __name__ == "__main__":
    asyncio.run(run_test())
import os
import streamlit as st
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import re
import speech_recognition as sr

st.set_page_config(page_title="Alexa+ City Service Agent", page_icon="🤖")

# --- CUSTOM CSS TO MATCH YOUR BROWN THEME ---
st.markdown("""
<style>
/* Style the buttons to match the brown brand color */
div.stButton > button:first-child {
    background-color: #8c7b6d !important;
    color: white !important;
    border: 2px solid #4a3f35 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
div.stButton > button:first-child:hover {
    background-color: #4a3f35 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 City Service Voice Agent")
st.write("Speak to update any city service page.")

if "draft_id" not in st.session_state:
    st.session_state.draft_id = None
if "draft_text" not in st.session_state:
    st.session_state.draft_text = None
if "city" not in st.session_state:
    st.session_state.city = ""
if "service" not in st.session_state:
    st.session_state.service = ""
if "message" not in st.session_state:
    st.session_state.message = ""

async def call_mcp_tool(tool_name, arguments):
    # Uses the Cloud URL if available, otherwise falls back to localhost
    url = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")
    
    try:
        async with streamable_http_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=arguments)
                return result.content[0].text
    except Exception as e:
        return f"Connection Error: {e}"

st.subheader("1. Speak or Type your request")
audio_value = st.audio_input("Record a voice message (e.g., 'Update Mumbai Plumber to say we are closed today')")

if audio_value:
    if st.button("Transcribe Audio"):
        with st.spinner("Listening..."):
            r = sr.Recognizer()
            try:
                audio_data = sr.AudioData(audio_value.read(), 16000, 2) 
                transcript = r.recognize_google(audio_data)
                st.success(f"Heard: **'{transcript}'**")
                
                # Smart extraction logic
                msg_match = re.search(r'(?:to say|saying|say|that)\s+(.*)', transcript, re.IGNORECASE)
                if msg_match:
                    st.session_state.message = msg_match.group(1).strip().capitalize()
                else:
                    st.session_state.message = transcript.strip().capitalize()
                
                # Try to guess city and service from the beginning of the sentence
                words = transcript.lower().replace("update", "").replace("change", "").split()
                if len(words) >= 2:
                    st.session_state.city = words[0].capitalize()
                    st.session_state.service = words[1].capitalize()
                    
            except Exception as e:
                st.error(f"Could not understand audio: {e}")

with st.form("details_form"):
    city_input = st.text_input("City", value=st.session_state.city)
    service_input = st.text_input("Service", value=st.session_state.service)
    message_input = st.text_area("Message to Display", value=st.session_state.message)
    submit = st.form_submit_button("Send to Agent")

if submit:
    with st.spinner("Finding page and drafting..."):
        response = asyncio.run(call_mcp_tool("find_and_draft_update", {
            "city": city_input, 
            "service": service_input, 
            "custom_message": message_input
        }))
        st.session_state.draft_text = response
        match = re.search(r'Draft ID is ([a-zA-Z0-9-]+)', response)
        if match:
            st.session_state.draft_id = match.group(1)

# Check if the WordPress widget passed a voice transcript
if "voice" in st.query_params:
    transcript = st.query_params["voice"]
    st.session_state.message = transcript
    # Clear the query param so it doesn't run twice
    st.query_params.clear() 
    st.rerun()

if st.session_state.draft_text:
    st.info(f"**Agent:** {st.session_state.draft_text}")
    
    # Changed the emoji to ✔
    if st.button("✔ Confirm & Publish to WordPress"):
        with st.spinner("Publishing to WordPress..."):
            confirm_response = asyncio.run(call_mcp_tool("confirm_and_publish", {"draft_id": st.session_state.draft_id}))
            st.success(f"**Agent:** {confirm_response}")
            st.session_state.draft_id = None
            st.session_state.draft_text = None
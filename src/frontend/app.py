# src/frontend/app.py
import streamlit as st
import asyncio
import sys
import os

# 1. Path Hack: Ensure Python knows where our 'src' folder is 
# This is required because we are running Streamlit from inside a subfolder.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agent.mcp_runner import mcp_session_manager
from src.agent.orchestrator import process_chat

# 2. Configure the UI layout
st.set_page_config(page_title="Epic EHR AI Assistant", page_icon="🏥", layout="centered")
st.title("Epic FHIR AI Assistant")
st.caption("Secure Clinical Workflow Automation via MCP")

# 3. Initialize the visual chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming message from the AI
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello Dr. Smith. I am securely connected to the Epic EHR network. How can I assist you with your patients today?"
    })

# Draw all past messages to the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Helper function to bridge Streamlit's sync world with our Async backend
async def fetch_ai_response(user_text: str):
    # This automatically boots up your FastMCP server, runs the query, and shuts it down safely!
    async with mcp_session_manager() as session:
        return await process_chat(user_text, session)

# 5. The Chat Input Box
if prompt := st.chat_input("E.g., 'Get the latest A1C labs for John and draft a quick note.'"):
    
    # Show what the user typed immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call the AI Engine and show a loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Securely accessing EHR database..."):
            try:
                # Run the orchestrator
                response = asyncio.run(fetch_ai_response(prompt))
                
                # Display the final clinical note/response
                st.markdown(response)
                
                # Save the AI's response to the visual history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"System Error: {str(e)}")
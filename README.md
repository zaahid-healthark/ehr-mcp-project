# Epic FHIR EHR Integration via Model Context Protocol (MCP)

## Overview
This project bridges the gap between state-of-the-art Large Language Models (LLMs) and healthcare infrastructure. By utilizing Anthropic's Model Context Protocol (MCP), we create a secure, standardized server that allows AI agents (like OpenAI's GPT-4o or Claude) to securely query Epic's FHIR APIs.

This enables automated clinical workflows, such as:
- Real-time patient data retrieval (Labs, Vitals).
- Automated, hospital-compliant clinical note generation.
- Context-aware ICD-10 billing code suggestions.

The ultimate business goal: Reduce physician documentation time ("pajama time") by up to 40% and improve billing accuracy.

---

## Architecture
The system is built on a modern Python stack using Separation of Concerns:

1. Frontend (`src/frontend`): A Streamlit chat interface for doctors to interact with the AI.
2. AI Agent (`src/agent`): Manages conversation state and OpenAI tool-calling logic.
3. MCP Server (`src/server`): A FastMCP server that translates AI tool requests into secure database queries.
4. FHIR Client (`src/server/fhir_client.py`): Handles OAuth2 authentication and raw HTTP requests to the Epic Developer Sandbox.

---

## Prerequisites
Before running this project, ensure you have the following installed on your machine:

- Python 3.9+
- Git
- An OpenAI API Key
- Epic FHIR Sandbox Credentials (Client ID and Private Key)

---

## Setup Guide (Windows)

### 1. Clone the Repository
```cmd
git clone https://github.com/YOUR_USERNAME/ehr-mcp-project.git
cd ehr-mcp-project
```

### 2. Create and Activate the Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory and add the following:

```
# AI Keys
OPENAI_API_KEY="sk-your-actual-openai-api-key-here"

# Epic FHIR Sandbox Credentials
EPIC_CLIENT_ID="your_epic_client_id_here"
EPIC_PRIVATE_KEY_PATH="/path/to/your/private_key.pem"
EPIC_FHIR_BASE_URL="https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"
```

Note: The .env file is included in .gitignore and will never be committed to GitHub.

---

## Project Structure

```
ehr-mcp-project/
├── .env
├── requirements.txt
└── src/
    ├── config/
    ├── server/
    ├── agent/
    └── frontend/
```

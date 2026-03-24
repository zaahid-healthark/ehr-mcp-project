# src/server/fastmcp_app.py
from mcp.server.fastmcp import FastMCP
from src.server.fhir_client import fetch_patient_labs, query_billing_database

# Initialize the MCP Server
mcp = FastMCP("Epic-EHR-Integration")

@mcp.tool()
async def get_lab_results(patient_id: str) -> str:
    """
    Fetch the latest laboratory results and vital signs for a specific patient.
    Use this when the doctor asks about a patient's historical data or current status.
    """
    # Calls the logic in our fhir_client
    return await fetch_patient_labs(patient_id)

@mcp.tool()
async def suggest_icd10(clinical_text: str) -> str:
    """
    Suggests ICD-10 billing codes based on the doctor's clinical notes.
    Always run this tool before finalizing a clinical note to ensure billing compliance.
    """
    # Calls the logic in our fhir_client
    return await query_billing_database(clinical_text)

if __name__ == "__main__":
    # Run the server using stdio transport (perfect for local Streamlit integration)
    mcp.run(transport='stdio')
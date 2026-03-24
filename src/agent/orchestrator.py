# src/agent/orchestrator.py
import json
from openai import AsyncOpenAI
from src.config.settings import config

# Initialize OpenAI Client securely using our config
client = AsyncOpenAI(api_key=config.openai_api_key)

async def process_chat(user_message: str, mcp_session) -> str:
    """
    The Brain: Takes a user message, talks to OpenAI, executes MCP tools if needed, 
    and returns the final clinical response.
    """
    # 1. Ask the MCP Server what tools it currently has available
    mcp_response = await mcp_session.list_tools()
    
    # 2. Translate MCP tools into OpenAI's required JSON format
    openai_tools = []
    for tool in mcp_response.tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })

    # 3. Setup the initial conversation history
    messages = [
        {
            "role": "system", 
            "content": "You are a highly capable medical AI assistant. Use the provided tools to securely fetch patient data from the EHR or query billing codes. Always be concise and professional."
        },
        {"role": "user", "content": user_message}
    ]

    # 4. First call to OpenAI: "Here is the user's prompt and the tools you can use."
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_tools
    )

    response_message = response.choices[0].message

    # 5. Did OpenAI decide to use a tool?
    if response_message.tool_calls:
        messages.append(response_message) # Save the AI's intent to history
        
        # Loop through and execute each tool OpenAI requested
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            # Print to terminal so we can see it working behind the scenes
            print(f"\n[SYSTEM] OpenAI requested tool: {tool_name}")
            print(f"[SYSTEM] Arguments: {tool_args}")
            
            # Tell our custom MCP Server to run the tool (e.g., fetch Epic data)
            result = await mcp_session.call_tool(tool_name, arguments=tool_args)
            
            # Extract the text data returned by the server
            tool_result_text = result.content[0].text if result.content else "No data."
            print(f"[SYSTEM] Data retrieved: {tool_result_text}\n")
            
            # Add the database result back into the chat history for OpenAI to read
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": tool_result_text
            })

        # 6. Second call to OpenAI: "Here is the database info you asked for. Now answer the user."
        final_response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final_response.choices[0].message.content
        
    # If no tools were needed, just return OpenAI's standard text reply
    return response_message.content
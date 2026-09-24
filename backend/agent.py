import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from backend.rag import query_knowledge_base
from backend.tools.it_tools import (
    reset_password_tool, 
    install_software_tool, 
    grant_access_tool, 
    request_hardware_tool
)

load_dotenv()

@tool
def search_it_policies_tool(query: str) -> str:
    """Search enterprise IT policies, software approval lists, and operating procedures."""
    return query_knowledge_base(query)

# Added request_hardware_tool to the tools list
tools = [
    reset_password_tool, 
    install_software_tool, 
    grant_access_tool, 
    search_it_policies_tool, 
    request_hardware_tool
]
tools_by_name = {t.name: t for t in tools}

# Using your specific model endpoint
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=os.environ.get("GOOGLE_API_KEY") 
)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = (
    "You are an Autonomous AI Agent for an Enterprise IT Helpdesk.\n"
    "Your job is to resolve L1 requests (password resets, software installs, access requests, hardware orders).\n"
    "Step 1: Check IT policies using 'search_it_policies_tool' to verify approval status.\n"
    "Step 2: If approved, invoke the matching execution tool.\n"
    "Step 3: If restricted or requires manager approval, notify the user clearly.\n"
    "Be direct, polite, and state every action completed."
)

def _extract_text(content) -> str:
    """Converts string or block-list responses into a clean string for SQLite."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
            elif isinstance(part, str):
                text_parts.append(part)
        return "\n".join(text_parts) if text_parts else str(content)
    return str(content)

def execute_it_agent(user_email: str, request_text: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Employee Email: {user_email}\nRequest: {request_text}")
    ]

    for _ in range(5):
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not hasattr(ai_msg, 'tool_calls') or not ai_msg.tool_calls:
            return _extract_text(ai_msg.content)

        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            selected_tool = tools_by_name[tool_name]
            tool_output = selected_tool.invoke(tool_args)
            
            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))

    return _extract_text(messages[-1].content)
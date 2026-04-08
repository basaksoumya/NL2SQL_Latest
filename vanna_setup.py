import os
from dotenv import load_dotenv

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService

load_dotenv()

# LLM
llm = GeminiLlmService(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash"   # ✅ FREE MODEL
)
# DB
runner = SqliteRunner("clinic.db")

# ✅ ONLY REQUIRED TOOLS (FIXED)
registry = ToolRegistry()
registry.tools = [
    RunSqlTool(runner),
    VisualizeDataTool()
]

# Memory
memory = DemoAgentMemory()

# User resolver
class DefaultUserResolver(UserResolver):
    async def resolve_user(self, ctx):
        return User(id="default")

resolver = DefaultUserResolver()

# Agent (NO system_prompt)
agent = Agent(
    llm_service=llm,
    tool_registry=registry,
    user_resolver=resolver,
    agent_memory=memory
)

def get_agent():
    return agent
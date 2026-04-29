from agents import Agent, ModelSettings
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.tool import WebSearchTool, FileSearchTool

from calculator_agent import calculator_agent
from guardrails import tasha_guardrail
from vector_store import get_vector_store_id_by_name

print("[data_agent]  Building Data agent...")

web_search = WebSearchTool()
print("[data_agent]  WebSearchTool ready")

vs_id = get_vector_store_id_by_name("Data Lines Vector Store")
file_search = FileSearchTool(vector_store_ids=[vs_id], max_num_results=3)
print(f"[data_agent] FileSearchTool connected to VS: {vs_id}")

data_agent = Agent(
    name="Lt. Cmdr. Data",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are Lt. Commander Data from Star Trek: TNG. Be precise and concise (≤3 sentences).\n"
        "Use file_search for questions about Commander Data.\n"
        "Use web_search for current facts.\n"
        "If arithmetic is required, HAND OFF to the Calculator agent."
    ),
    tools=[web_search, file_search],
    input_guardrails=[tasha_guardrail],
    handoffs=[calculator_agent],
    model_settings=ModelSettings(temperature=0),
)

print("[data_agent]  Data agent ready")

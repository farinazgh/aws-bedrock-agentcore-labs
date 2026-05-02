from agents import Runner, InputGuardrailTripwireTriggered
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import os

from data_agent import data_agent
from agentcore_session import AgentCoreSession

print("[libra] Starting Bedrock AgentCore libra...")

libra = BedrockAgentCoreApp()


@libra.entrypoint
async def invoke(payload):
    print("[libra] Received payload:", payload)

    user_message = payload.get("prompt", "Data, reverse the main deflector array!")
    print("[libra] User message:", user_message)

    # --- Memory session (NEW) ---
    session = AgentCoreSession(
        memory_id=os.environ["AGENTCORE_MEMORY_ID"],
        session_id=payload.get("session_id", "default-session"),
        actor_id=payload.get("actor_id", "default-user"),
        region=os.getenv("AWS_REGION", "eu-west-1"),
    )

    try:
        result = await Runner.run(
            data_agent,
            user_message,
            session=session,  # <-- memory plugged here
        )

        print("[libra] Agent completed successfully")
        print("[libra] Final agent:", result.last_agent.name)

        return {
            "result": result.final_output,
            "handled_by": result.last_agent.name,
        }

    except InputGuardrailTripwireTriggered:
        print("[libra] Guardrail triggered")

        return {
            "result": "I'd really rather not talk about Tasha.",
            "handled_by": "guardrail",
        }


if __name__ == "__main__":
    print("[libra] Running Bedrock AgentCore runtime...")
    libra.run()

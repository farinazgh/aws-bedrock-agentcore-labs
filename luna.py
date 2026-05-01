from agents import Runner, InputGuardrailTripwireTriggered
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from data_agent import data_agent

print("[luna] Starting Bedrock AgentCore luna...")

luna = BedrockAgentCoreApp()


@luna.entrypoint
async def invoke(payload):
    print("[luna] Received payload:", payload)

    user_message = payload.get("prompt", "Data, reverse the main deflector array!")

    print("[luna] User message:", user_message)

    try:
        result = await Runner.run(data_agent, user_message)

        print("[luna] Agent completed successfully")
        print("[luna] Final agent:", result.last_agent.name)

        return {
            "result": result.final_output,
            "handled_by": result.last_agent.name,
        }

    except InputGuardrailTripwireTriggered:
        print("[luna] Guardrail triggered")

        return {
            "result": "I'd really rather not talk about Tasha.",
            "handled_by": "guardrail",
        }


if __name__ == "__main__":
    print("[luna] Running Bedrock AgentCore runtime...")
    luna.run()

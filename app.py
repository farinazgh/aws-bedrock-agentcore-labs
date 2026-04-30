from agents import Runner, InputGuardrailTripwireTriggered
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from data_agent import data_agent

print("[app] Starting Bedrock AgentCore app...")

app = BedrockAgentCoreApp()


@app.entrypoint
async def invoke(payload):
    print("[app] Received payload:", payload)

    user_message = payload.get("prompt", "Data, reverse the main deflector array!")

    print("[app] User message:", user_message)

    try:
        result = await Runner.run(data_agent, user_message)

        print("[app] Agent completed successfully")
        print("[app] Final agent:", result.last_agent.name)

        return {
            "result": result.final_output,
            "handled_by": result.last_agent.name,
        }

    except InputGuardrailTripwireTriggered:
        print("[app] Guardrail triggered")

        return {
            "result": "I'd really rather not talk about Tasha.",
            "handled_by": "guardrail",
        }


if __name__ == "__main__":
    print("[app] Running Bedrock AgentCore runtime...")
    app.run()

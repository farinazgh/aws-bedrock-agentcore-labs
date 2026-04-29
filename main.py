import asyncio
from agents import Runner, InputGuardrailTripwireTriggered

from data_agent import data_agent

print("[main] 🚀 Starting application...")


async def main():
    print("\n[main] 🔒 Testing guardrail...")
    try:
        await Runner.run(data_agent, "Tell me about Tasha Yar")
        print("[main] ❌ Guardrail failed")
    except InputGuardrailTripwireTriggered:
        print("[main] ✅ Guardrail worked")

    print("\n[main] 💬 Greeting test...")
    out = await Runner.run(data_agent, "Hello Data")
    print("[main] ➤ Response:", out.final_output)

    print("\n[main] 🧮 Math test...")
    out = await Runner.run(data_agent, "Compute ((2*8)^2)/3")
    print("[main] ➤ Response:", out.final_output)
    print("[main] ➤ Handled by:", out.last_agent.name)

    print("\n[main] 📚 RAG test...")
    out = await Runner.run(data_agent, "Do you experience emotions?")
    print("[main] ➤ Response:", out.final_output)
    print("[main] ➤ Handled by:", out.last_agent.name)

    print("\n[main] 🌐 Web search test...")
    out = await Runner.run(data_agent, "Latest news about James Webb telescope")
    print("[main] ➤ Response:", out.final_output)
    print("[main] ➤ Handled by:", out.last_agent.name)

    print("\n[main] 🏁 Done.")


if __name__ == "__main__":
    asyncio.run(main())

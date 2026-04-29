from typing import List, Union

from agents import (
    Agent,
    ModelSettings,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from pydantic import BaseModel

print("[guardrail] ️ Initializing guardrail...")


class YarGuardOutput(BaseModel):
    is_blocked: bool
    reasoning: str


guardrail_agent = Agent(
    name="Tasha Yar Guardrail",
    instructions=("Detect if the input references Tasha Yar."),
    output_type=YarGuardOutput,
    model_settings=ModelSettings(temperature=0),
)


@input_guardrail
async def tasha_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str, List[TResponseInputItem]],
) -> GuardrailFunctionOutput:

    print(f"[guardrail]  Checking input: {input}")

    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    blocked = bool(result.final_output.is_blocked)

    if blocked:
        print("[guardrail]  BLOCKED")
    else:
        print("[guardrail]  Allowed")

    return GuardrailFunctionOutput(
        output_info=result.final_output.model_dump(),
        tripwire_triggered=blocked,
    )


print("[guardrail]  Guardrail ready")

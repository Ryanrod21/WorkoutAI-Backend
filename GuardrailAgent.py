from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput
import json
import logging

# -----------------------------
# 1️⃣ Guardrail instructions
# -----------------------------

INSTRUCTIONS = """
You analyze user messages and decide if they are allowed.

Allowed topics:
- Workouts
- Fitness
- Exercise routines
- Training goals
- Nutrition basics
- Workout progression (updating or progressing existing plans)

Disallowed topics:
- Cars, politics, finance
- Medical diagnosis or treatment
- Violence or self-harm
- Illegal or dangerous activities
- Anything unrelated to fitness

Return:
- is_out_of_scope: true if the message should be blocked
- reason: short explanation
"""

# -----------------------------
# 2️⃣ Output schema
# -----------------------------

class WorkoutGuardrailResult(BaseModel):
    is_out_of_scope: bool
    reason: str

# -----------------------------
# 3️⃣ Guardrail agent
# -----------------------------

guardrail_agent = Agent(
    name="Workout Guardrail Agent",
    instructions=INSTRUCTIONS,
    output_type=WorkoutGuardrailResult,
    model="gpt-4o-mini",
)

# -----------------------------
# 4️⃣ Guardrail function (tripwire)
# -----------------------------

@input_guardrail
async def workout_scope_guardrail(ctx, agent, message):
    # If message is a dict (like from FastAPI), read type directly
    if isinstance(message, dict):
        request_type = message.get("type")
        if request_type in {"workout_generation", "workout_progression"}:
            return GuardrailFunctionOutput(
                output_info={"reason": "Internal workout request allowed"},
                tripwire_triggered=False,
            )

    # If message is a string, try parsing JSON
    elif isinstance(message, str):
        try:
            msg_data = json.loads(message)
            request_type = msg_data.get("type")
            if request_type in {"workout_generation", "workout_progression"}:
                return GuardrailFunctionOutput(
                    output_info={"reason": "Internal workout request allowed"},
                    tripwire_triggered=False,
                )
        except Exception:
            pass

    # fallback to LLM for other cases
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info={"reason": result.final_output.reason},
        tripwire_triggered=result.final_output.is_out_of_scope,
    )

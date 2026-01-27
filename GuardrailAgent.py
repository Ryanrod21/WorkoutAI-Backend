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
    """
    Guardrail that allows both new workouts and progression inputs.
    """

    # Try to parse message as JSON to detect type
    try:
        msg_data = json.loads(message)
        request_type = msg_data.get("type", "")
    except Exception:
        # If not JSON, fallback to original agent check
        request_type = ""

    # ✅ Allow progression requests explicitly
    if request_type == "workout_progression":
        logging.info("Guardrail allowed workout progression input")
        return GuardrailFunctionOutput(
            output_info={"reason": "Workout progression detected, allowed"},
            tripwire_triggered=False,
        )

    # ✅ Allow normal workout_generation requests
    if request_type == "workout_generation":
        logging.info("Guardrail allowed new workout generation")
        return GuardrailFunctionOutput(
            output_info={"reason": "New workout detected, allowed"},
            tripwire_triggered=False,
        )

    # Otherwise, fallback to the agent's normal check
    result = await Runner.run(
        guardrail_agent,
        message,
        context=ctx.context,
    )

    return GuardrailFunctionOutput(
        output_info={"reason": result.final_output.reason},
        tripwire_triggered=result.final_output.is_out_of_scope,
    )

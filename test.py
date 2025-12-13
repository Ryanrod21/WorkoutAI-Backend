from pydantic import BaseModel, Field
from agents import Agent

# -------------------------------
# Instructions (constant)
# -------------------------------
INSTRUCTIONS = (
    "You are a Workout Plan Generator agent.\n"
    "Your job:\n"
    "- Create a concise workout plan for the user.\n"
    "- Use the following user info: days, goal, train.\n"
    "- Return ONLY raw JSON.\n"
    "- Do NOT wrap in markdown or code fences.\n"
    "- Respond with valid JSON ONLY in this format:\n"
    "{\n"
    '  "plan_summary": "string",\n'
    '  "exercises": [\n'
    "    {\n"
    '      "name": "string",\n'
    '      "reps_sets": "string",\n'
    '      "notes": "string"\n'
    "    }\n"
    "  ]\n"
    "}"
)

# -------------------------------
# Output model
# -------------------------------
class Exercise(BaseModel):
    name: str = Field(description="Name of the exercise")
    reps_sets: str = Field(description="Reps and sets for the exercise")
    notes: str = Field(description="Additional notes or tips for the exercise")

class PlanOutput(BaseModel):
    plan_summary: str = Field(description="A concise summary of the workout plan")
    exercises: list[Exercise] = Field(description="List of exercises included in the plan")

# -------------------------------
# Agent definition
# -------------------------------
WorkoutPlanAgent = Agent(
    name="WorkoutPlanAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=PlanOutput,
)

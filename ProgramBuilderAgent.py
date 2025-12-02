from agents import Agent, ModelSettings
from pydantic import BaseModel, Field

INSTRUCTIONS = """
    You are the Program Builder Agent. Take the exercises provided and organize
    a workout plan with sets, reps, and rest intervals.
    Only have a total of 3 workouts
    """

class ProgramData(BaseModel):
    plan: str = Field(description="The structured workout plan with exercises, sets, reps")


ProgramBuilderAgent = Agent(
    name="ProgramBuilderAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ProgramData
)
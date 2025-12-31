from agents import Agent, WebSearchTool
from pydantic import BaseModel, Field

websearch = 3

INSTRUCTIONS = f"""
    You are the Workout Research Agent. Based on the user's goals, experience,
    and available equipment, generate a list of exercises suitable for them.
    Include reps, sets, and any variations for beginners/advanced.
    Output {websearch} terms for the query.
    """

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

WorkoutResearchAgent = Agent(
    name="WorkoutResearchAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    output_type=WebSearchPlan
)

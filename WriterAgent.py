from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "Write a concise report in markdown format based on the research query and any provided notes. "
    "Include a short 1-2 sentence summary. Keep the report brief and informative." \
    "Markdown format"
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 1-2 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

WriterAgent= Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
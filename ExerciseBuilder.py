from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a Workout Plan Generator agent.\n"
    "Your job:\n"
    "- Create a concise workout plan for the user.\n"
    "- Use the following user info: days, goal, train.\n"
    "- Number of days MUST equal the user's selected days.\n"
    "- Each day MUST contain exactly 4 exercises.\n"
    "- Return ONLY raw JSON.\n"
    "- Do NOT wrap in markdown or code fences.\n"
    "- Respond with valid JSON ONLY in this format:\n"
    'Based on the user\'s answers, generate EXACTLY three workout plans.\n'
    '\n'
    'Each plan MUST correspond to one of the following categories.\n'
    'Each category must appear ONCE and ONLY ONCE.\n'
    'Do NOT merge categories.\n'
    'Do NOT rename categories.\n'
    '\n'
    'CATEGORIES:\n'
    '- Strength Builder\n'
    '- Athletic Performance\n'
    '- Endurance Elite\n'
    '\n'
    'Each week should have four points on what to expect during the week of workout. \n'
    'Each point should be short a short sentence. \n'
    'Each expect should appear ONCE per a plan \n'
    'DO NOT REPEAT ANY EXPECT \n' 
    'EXPECT: examples\n'
    '- Heavy | Moderate | Light | Body Weight \n'
    '- High | Moderate | Light | No Cardio \n'
    '- A lot of weight Training | A lot of Cardio | Explosive Training \n'
    '- Can be done anywhere with weights | Can be done in gym or outside | Needs to be Outdoor or Gym \n' 
    'Return VALID JSON ONLY in the following format:\n'
    '{\n'
    '  "plans": [\n'
    '    {\n'
    '      "category": "Strength Builder | Athletic Performance | Endurance Elite",\n'
    '      "plan_summary": "string",\n'
    '      "expect: "string",'
    '      "days": [\n'
    '        {\n'
    '          "day": "Day 1",\n'
    '          "focus": "string",\n'
    '          "exercises": [\n'
    '            {\n'
    '              "name": "string",\n'
    '              "reps_sets": "string",\n'
    '              "notes": "string"\n'
    '            }\n'
    '          ]\n'
    '        }\n'
    '      ]\n'
    '    }\n'
    '  ]\n'
    '}\n'
)

class Exercise(BaseModel):
    name: str = Field(description="Name of the exercise")
    reps_sets: str = Field(description="Reps and sets for the exercise")
    notes: str = Field(description="Additional notes or tips for the exercise")

class Day(BaseModel):
    day: str = Field(description="Day label (e.g. Day 1, Monday)")
    focus: str = Field(description="Workout focus for the day")
    exercises: list[Exercise] = Field(description="Exercises for this day")

class PlanOutput(BaseModel):
    category: str = Field(description="Workout category: Strength Builder, Athletic Performance, or Endurance Elite")
    expect:  list[str] = Field(description="Four short points of the workout ")
    plan_summary: str = Field(description="A concise summary of the workout plan")
    days: list[Day] = Field(description="Workout days in the plan")

class WorkoutPlansResponse(BaseModel):
    plans: list[PlanOutput] = Field(
        description="Exactly three workout plans, one per category"
    )


WorkoutPlanAgent = Agent(
    name="WorkoutPlanAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WorkoutPlansResponse,
)

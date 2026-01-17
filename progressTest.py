import asyncio
from WorkoutCoach import ProgressionCoach
from dotenv import load_dotenv
import json


# Load API key before anything else
load_dotenv()


sample_previous_week = [
    {
        "category": "Strength Builder",
        "day": "Day 1",
        "exercises": [
            {"name": "Squat", "sets": 3, "reps": 10, "weight": 100},
            {"name": "Bench Press", "sets": 3, "reps": 10, "weight": 80},
            {"name": "Deadlift", "sets": 3, "reps": 8, "weight": 120},
            {"name": "Pull-ups", "sets": 3, "reps": 12, "weight": 0},
        ],
    },
    {
        "category": "Athletic Performance",
        "day": "Day 2",
        "exercises": [
            {"name": "Box Jump", "sets": 3, "reps": 10, "weight": 0},
            {"name": "Sprint", "sets": 5, "reps": 20, "weight": 0},
            {"name": "Medicine Ball Throw", "sets": 3, "reps": 12, "weight": 10},
            {"name": "Lunge", "sets": 3, "reps": 10, "weight": 20},
        ],
    },
]

feedback = "too easy"
goals_update = ["Increase strength", "More explosive movements"]


progression_agent = ProgressionCoach()


async def test_progression_agent():
    # Run the progression agent
    next_week = await progression_agent.run(
        previous_week=sample_previous_week,
        feedback=feedback,
        goals_update=goals_update
    )

    # Convert list of Pydantic models to list of dicts
    next_week_dicts = [plan.dict() for plan in next_week]

    # Serialize to JSON string
    json_output = json.dumps(next_week_dicts, indent=2)

    # Print proper JSON
    print(json_output)

# Run the async test
asyncio.run(test_progression_agent())
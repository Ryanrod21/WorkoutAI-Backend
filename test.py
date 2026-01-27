import asyncio
import logging
from dotenv import load_dotenv

from WorkoutCoach import ProgressionCoach
# adjust import paths ↑ to match your project
# from agents.progression_agent import ProgressionAgent (used internally)

logging.basicConfig(level=logging.INFO)

load_dotenv()  # Load environment variables from .env file


async def main():
    coach = ProgressionCoach()

    # 👇 Sample previous week data (input to agent)
    previous_week = {
        "week": 1,
        "category": "strength",
        "plan_summary": "3-day full body strength program",
        "days": 3,
        "workouts": [
            {"day": 1, "focus": "Upper Body"},
            {"day": 2, "focus": "Lower Body"},
            {"day": 3, "focus": "Full Body"},
        ]
    }

    # 🔥 Call ProgressionCoach → Agent
    result = await coach.run(
        previous_week=previous_week,
        difficulty="moderate",
        soreness="low",
        completed=True,
        progression="increased weights on compounds",
        feedback="Felt strong all week, recovery was good"
    )

    # 🖨️ Print agent output
    print("\n✅ Agent Result:")
    for plan in result:
        print(plan)


if __name__ == "__main__":
    asyncio.run(main())

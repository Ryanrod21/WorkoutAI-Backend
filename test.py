import asyncio
import json
from dataclasses import asdict
from dotenv import load_dotenv

# Load API key before anything else
load_dotenv()

from WorkoutCoach import WorkoutCoach
from ExerciseBuilder import PlanOutput


async def main():
    coach = WorkoutCoach()

    # 🔧 Dummy / test input
    days = 4
    goal = "muscle gain"
    train = "gym"
    n = 1  # start with 1 for easier debugging

    results = await coach.run(days, goal, train, n)

    print("\n✅ WORKOUT COACH RESPONSE\n")

    for i, plan in enumerate(results, 1):
        print(f"--- Plan {i} ---")

        # If PlanOutput is a dataclass
        try:
            print(json.dumps(asdict(plan), indent=2))
        except TypeError:
            # If it's a Pydantic model
            print(json.dumps(plan.model_dump(), indent=2))

        print()


if __name__ == "__main__":
    asyncio.run(main())

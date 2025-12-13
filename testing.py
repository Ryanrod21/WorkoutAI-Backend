import asyncio
from WorkoutCoach import WorkoutCoach
from dotenv import load_dotenv

load_dotenv()

coach = WorkoutCoach()

async def test():
    results = await coach.run(days=3, goal="lose weight", train="gym", n=3)
    for i, plan in enumerate(results, 1):
        print(f"\n--- Plan {i} ---")
        print(plan.plan_summary)
        for ex in plan.exercises:
            print(f"{ex.name}: {ex.reps_sets} ({ex.notes})")

if __name__ == "__main__":
    asyncio.run(test())

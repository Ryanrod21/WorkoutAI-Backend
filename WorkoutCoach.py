import asyncio
from typing import List
from test import WorkoutPlanAgent, PlanOutput
from agents import Runner  # Runner is needed to execute the agent

class WorkoutCoach:
    async def run(self, days: int, goal: str, train: str, n: int = 3) -> List[PlanOutput]:
        # Run n tasks in parallel
        tasks = [self.plan_search(days, goal, train) for _ in range(n)]
        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(self, days: int, goal: str, train: str) -> PlanOutput:
        # Combine inputs into a single string
        input_text = f"days={days}, goal={goal}, train={train}"
        # Run the agent using Runner.run
        result = await Runner.run(WorkoutPlanAgent, input_text)
        return result.final_output  # This will be a PlanOutput object

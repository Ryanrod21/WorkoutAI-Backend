import asyncio
from typing import List
from ExerciseBuilder import WorkoutPlanAgent, WorkoutPlansResponse
from agents import Runner  # Runner is needed to execute the agent

class WorkoutCoach:
    async def run(self, days, goal, train, experience, minutes):
        # Call plan_search once directly — no wrapping in a list
        result = await self.plan_search(days, goal, train, experience, minutes)
        return result.dict()  # returns { "plans": [plan1, plan2, plan3] }

    async def plan_search(self, days, goal, train, experience, minutes):
        input_text = f"days={days}, goal={goal}, train={train}, experience={experience}, minutes={minutes}"
        result = await Runner.run(WorkoutPlanAgent, input_text)
        return result.final_output  # WorkoutPlansResponse object

import asyncio
from typing import List
from ExerciseBuilder import WorkoutPlanAgent, WorkoutPlansResponse
from Progression import WorkoutProgressionAgent
from agents import Runner  # Runner is needed to execute the agent

class WorkoutCoach:
    async def run(self, days: int, goal: str, train: str, experience: str, minutes: int):
        # Run n tasks in parallel
        tasks = [self.plan_search(days, goal, train, experience, minutes)]
        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(self, days: int, goal: str, train: str, experience: str, minutes: int,) -> WorkoutPlansResponse:
        # Combine inputs into a single string
        input_text = f"days={days}, goal={goal}, train={train} experience={experience} minutes={minutes}"
        # Run the agent using Runner.run
        result = await Runner.run(WorkoutPlanAgent, input_text)
        return result.final_output 

class ProgressionCoach:
    async def run(self, previous_week, feedback=None, goals_update=None):
        # Run n tasks in parallel (optional)
        tasks = [self.plan_search(previous_week, feedback, goals_update)]
        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(self, previous_week, feedback=None, goals_update=None):
        # Combine inputs into a single string or structured prompt
        input_text = f"previous_week={previous_week}, feedback={feedback}, goals_update={goals_update}"

        # Use your Runner to execute the agent
        result = await Runner.run(WorkoutProgressionAgent, input_text)
        return result.final_output

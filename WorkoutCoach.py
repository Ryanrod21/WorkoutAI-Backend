import asyncio
from typing import List
from ExerciseBuilder import WorkoutPlanAgent, WorkoutPlansResponse
from Progression import WorkoutProgressionAgent
from agents import Runner  # Runner is needed to execute the agent

class WorkoutCoach:
    async def run(self, days: int, goal: str, location: str, experience: str, minutes: int, week: int = 1):
        tasks = [self.plan_search(days, goal, location, experience, minutes, week)]
        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(self, days: int, goal: str, location: str, experience: str, minutes: int, week: int) -> WorkoutPlansResponse:
        input_text = f"week={week}, days={days}, goal={goal}, location={location}, experience={experience}, minutes={minutes}"
        result = await Runner.run(WorkoutPlanAgent, input_text)
        return result.final_output


class ProgressionCoach:
    async def run(self, previous_week, difficulty=None, soreness=None, completed=None, progression=None, feedback=None):
        import logging
        logging.info(f"Received previous_week: {previous_week}")
        if "plans" not in previous_week or not previous_week["plans"]:
            logging.warning("No plans found, returning empty list")
            return []
        # generate dummy next week plans for testing
        next_week_plans = [{"plan_summary": "Test Plan", "category": "Strength Builder", "expect": ["Exercise A"]}]
        return next_week_plans


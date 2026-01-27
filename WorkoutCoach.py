import asyncio
from typing import List
from ExerciseBuilder import WorkoutPlanAgent, WorkoutPlansResponse
from Progression import WorkoutProgressionAgent
from agents import Runner  # Runner is needed to execute the agent
import logging

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
    async def run(
        self, previous_week, difficulty=None, soreness=None, completed=None, progression=None, feedback=None
    ):
        logging.info(f"Received previous_week: {previous_week}")  # <- log input

        plans = previous_week.get("plans")
        if not plans:
            logging.warning("No plans found in previous_week")
            return []

        logging.info(f"Plans found: {plans}")  # <- log plans array

        # Generate the next week's plans
        next_week_plans = []
        for day in plans:
            next_week_plans.append({
                "plan_summary": f"Next week plan for {day.get('day', 'Day')}",
                "category": previous_week.get("category", "General"),
                "expect": ["Follow progression", "Maintain consistency"]
            })

        logging.info(f"Next week plans generated: {next_week_plans}")  # <- log output
        return next_week_plans



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
    async def run(
        self,
        previous_week: dict,
        difficulty=None,
        soreness=None,
        completed=None,
        progression=None,
        feedback=None
    ):
        import logging
        logging.info(f"Progressing plan: {previous_week}")

        # ✅ Validate input
        if not isinstance(previous_week, dict):
            logging.error("previous_week must be a dict")
            return []

        if "plan_summary" not in previous_week:
            logging.error("Missing plan_summary in previous_week")
            return []

        # ✅ Build next week's plan based on previous
        next_plan = {
            "week": previous_week.get("week", 1) + 1,
            "category": previous_week.get("category"),
            "plan_summary": previous_week["plan_summary"],
            "expect": list(previous_week.get("expect", [])),
            "days": previous_week.get("days"),
            "adjustments": {
                "difficulty": difficulty,
                "soreness": soreness,
                "completed": completed,
                "progression": progression,
                "feedback": feedback,
            }
        }

        return [next_plan]



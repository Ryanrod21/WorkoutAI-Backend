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
        self,
        previous_week: dict,
        difficulty=None,
        soreness=None,
        completed=None,
        progression=None,
        feedback=None,
        week: int = None,
        preference: dict = None,
        day_status: dict = None,
    ):
        """
        Entry point for progressing a workout plan using an AI agent.
        Mirrors WorkoutCoach.run().
        """

        tasks = [
            self.plan_search(
                previous_week,
                difficulty,
                soreness,
                completed,
                progression,
                feedback,
                week,
                preference,
                day_status
            )
        ]

        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(
        self,
        previous_week: dict,
        difficulty=None,
        soreness=None,
        completed=None,
        progression=None,
        feedback=None,
        week: int = None,
        preference: dict = None,
        day_status: dict = None,
    ):
        """
        Sends previous week's plan + feedback to the agent.
        Agent is responsible for generating 3 workout plans.
        """

        logging.info("Running ProgressionAgent")

        # ✅ Validate input
        if not isinstance(previous_week, dict):
            logging.error("previous_week must be a dict")
            return []

        # Determine next week number
        next_week = week or previous_week.get("week", 1) + 1

        # 🧠 Build agent input (THIS is what the agent sees)
        input_text = f"""
        next_week={next_week}
        previous_week={previous_week}
        difficulty={difficulty}
        soreness={soreness}
        completed={completed}
        progression={progression}
        feedback={feedback}
        preference={preference}
        day_status={day_status}
        """

        # 🔥 Run the agent (this is what enables 3 workouts)
        result = await Runner.run(WorkoutProgressionAgent, input_text)

        # Agent should return a LIST of 3 workout plans
        return result.final_output

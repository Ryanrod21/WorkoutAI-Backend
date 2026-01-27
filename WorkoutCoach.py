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
    ):
        """
        Entry point for progressing a workout plan.
        Mirrors WorkoutCoach.run():
        - Creates async tasks
        - Gathers results
        - Returns the final output
        """

        # Create async task for generating the next week's plan
        tasks = [
            self.plan_search(
                previous_week,
                difficulty,
                soreness,
                completed,
                progression,
                feedback
            )
        ]

        # Run all tasks concurrently (scales well if more tasks are added later)
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
    ):
        """
        Core logic for generating the next week's workout plan.
        Uses the previous week's plan and user feedback to build progression.
        """

        # Log incoming plan for debugging and traceability
        logging.info(f"Progressing plan: {previous_week}")

        # ✅ Validate that previous_week is the correct type
        if not isinstance(previous_week, dict):
            logging.error("previous_week must be a dict")
            return []

        # ✅ Ensure required data exists
        if "plan_summary" not in previous_week:
            logging.error("Missing plan_summary in previous_week")
            return []

        # ✅ Construct the next week's plan
        next_plan = {
            # Increment week number (default to week 1 if missing)
            "week": previous_week.get("week", 1) + 1,

            # Carry over plan category (e.g. strength, hypertrophy, conditioning)
            "category": previous_week.get("category"),

            # Keep the original plan summary as the base template
            "plan_summary": previous_week["plan_summary"],

            # Copy expectations to avoid mutating original data
            "expect": list(previous_week.get("expect", [])),

            # Preserve number of training days
            "days": previous_week.get("days"),

            # Store user feedback and progression signals
            "adjustments": {
                "difficulty": difficulty,     # How hard the plan felt
                "soreness": soreness,         # Muscle soreness level
                "completed": completed,       # % or boolean completion
                "progression": progression,   # Strength/endurance progress
                "feedback": feedback,         # Free-form user notes
            }
        }

        # Return the next plan (single item, gathered by run())
        return next_plan
 



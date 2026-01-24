import asyncio
from typing import List
from ExerciseBuilder import WorkoutPlanAgent, WorkoutPlansResponse
from Progression import WorkoutProgressionAgent
from agents import Runner  # Runner is needed to execute the agent

class WorkoutCoach:
    async def run(self, days: int, goal: str, location: str, experience: str, minutes: int):
        # Run n tasks in parallel
        tasks = [self.plan_search(days, goal, location, experience, minutes)]
        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(self, days: int, goal: str, location: str, experience: str, minutes: int,) -> WorkoutPlansResponse:
        # Combine inputs into a single string
        input_text = f"days={days}, goal={goal}, location={location} experience={experience} minutes={minutes}"
        # Run the agent using Runner.run
        result = await Runner.run(WorkoutPlanAgent, input_text)
        return result.final_output 

class ProgressionCoach:
    async def run(self, previous_week, feedback=None, day_status=None, difficulty=None, soreness=None ,completed=None, progression=None,):
        tasks = [
            self.plan_search(
                previous_week,
                feedback,
                day_status,
                difficulty,
                soreness,
                completed,
                progression,
            )
        ]
        results = await asyncio.gather(*tasks)
        return results

    async def plan_search(self, previous_week, feedback=None, day_status=None, difficulty=None, soreness=None ,completed=None, progression=None,):
        input_text = (
            f"previous_week={previous_week}, "
            f"feedback={feedback}, "
            f"day_status={day_status}, "
            f"difficulty={difficulty}, "
            f"soreness={soreness}, "
            f"completed={completed}, "
            f"progression={progression}"
        )

        result = await Runner.run(WorkoutProgressionAgent, input_text)
        return result.final_output


import asyncio
from agents import Runner, trace, gen_trace_id
from WorkoutResearchAgent import WorkoutResearchAgent, WebSearchPlan
from ProgramBuilderAgent import ProgramBuilderAgent, ProgramData
from WriterAgent import WriterAgent, ReportData


class GymManager:

    async def run(self, user_input: str):
        trace_id = gen_trace_id()

        with trace("GymCoach trace", trace_id=trace_id):
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

            search_plan = await self.plan_searches(user_input)
            yield f"Planned {len(search_plan.searches)} searches."

            search_results = await self.perform_searches(search_plan)
            yield "All searches completed."

            program_data = await self.build_program(search_results)
            yield "Workout program built."

            final_plan = await self.write_final_plan(user_input, program_data)
            yield "Final polished workout plan ready."

            yield final_plan.markdown_report

    # -----------------------------------------------------
    # SUPPORT FUNCTIONS
    # -----------------------------------------------------

    async def plan_searches(self, user_input: str) -> WebSearchPlan:
        result = await Runner.run(WorkoutResearchAgent, user_input)
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """
        Perform searches for all items in the search plan using self.search().
        Tracks progress and filters out None results.
        """
        print("Starting searches...")
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []

        # Use asyncio.as_completed to process tasks as they finish
        for i, task in enumerate(asyncio.as_completed(tasks), start=1):
            result = await task
            if result is not None:
                results.append(result)
            print(f"Searches completed: {i}/{len(tasks)}")

        print("All searches done.")
        return results

    async def search(self, item) -> str | None:
        """
        Perform a single search for an item.
        Returns the result as string, or None if an error occurs.
        """
        try:
            result = await Runner.run(WorkoutResearchAgent, item.query)
            return str(result.final_output)
        except Exception as e:
            print(f"Search failed for '{item.query}': {e}")
            return None

    async def build_program(self, search_results) -> ProgramData:
        """
        Build program using research results (not search_plan).
        """
        combined = "\n".join([str(r) for r in search_results])
        result = await Runner.run(ProgramBuilderAgent, combined)
        print("Building Program")
        return result.final_output_as(ProgramData)

    async def write_final_plan(self, query: str, program_data: ProgramData) -> ReportData:
        print("Writing Program")
        prompt = f"Here is the full program for: {query}\n\n{program_data}"
        result = await Runner.run(WriterAgent, prompt)
        print("Done !")
        return result.final_output_as(ReportData)

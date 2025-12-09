import asyncio
from agents import Agent, Runner 
from dotenv import load_dotenv

load_dotenv()


async def testagent(days, goal, train):
    instructions = f"Make a short sentence using days={days}, goal={goal}, train={train}"
    agent = Agent(name="TestAgent", 
                  instructions=instructions, 
                  model="gpt-4o-mini")

    # Combine all inputs into a single string
    input_text = f"{days}, {goal}, {train}"

    result = await Runner.run(agent, input_text)  # pass as single argument
    return result.final_output



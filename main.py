import gradio as gr
from ManagerAgent import GymManager
from dotenv import load_dotenv

load_dotenv(override=True)

manager = GymManager()

async def generate_workout(user_input: str):
    async for step in manager.run(user_input):
        yield str(step)  # yield each step for live updates


with gr.Blocks() as demo:
    gr.Markdown("## 💪 AI Gym Coach")
    gr.Markdown("Enter your fitness goals below. Your personalized plan will appear underneath.")

    user_box = gr.Textbox(
        label="Your Fitness Goals",
        placeholder="Example: Build muscle, 4x a week, gym access",
        lines=2
    )
    generate_btn = gr.Button("Generate Plan")

    # Use Markdown for output so formatting shows
    result_box = gr.Markdown()

    # Click OR press Enter
    generate_btn.click(generate_workout, inputs=user_box, outputs=result_box)
    user_box.submit(generate_workout, inputs=user_box, outputs=result_box)


demo.launch(inbrowser=True)

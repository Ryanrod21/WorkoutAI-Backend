from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel
from WorkoutCoach import WorkoutCoach, WorkoutPlansResponse, ProgressionCoach


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://gymai-u2km.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Gym Coach API running!"}

# @app.get("/workout")
# async def generate_workout(query: str):
#     # Call your GymManager here
    
#     return {"workout": f"Generated plan for: {query}"}


class Input(BaseModel):
    days: int
    goal: str
    train: str
    experience: str
    minutes: int

# Instantiate the coach
coach = WorkoutCoach()

@app.post("/agent", response_model=List[WorkoutPlansResponse])
async def run_agent(data: Input):
    """
    Receives frontend input and returns multiple structured workout plans.
    """
    try:
        results = await coach.run(data.days, data.goal, data.train, data.experience, data.minutes)
        return results
    except Exception as e:
        return {"error": str(e)}


class ProgressionInput(BaseModel):
    user_id: int

    # Structured answers (easy for the agent to reason with)
    difficulty: Optional[str] = None
    soreness: Optional[str] = None
    completed: Optional[str] = None
    progression: Optional[str] = None

    # Free text (still useful!)
    feedback: Optional[str] = None


progression_agent = ProgressionCoach()

@app.post("/progression", response_model=List[dict])
async def run_progression_agent(data: ProgressionInput):
    try:
        # No DB, just use the frontend-provided data
        next_week = await progression_agent.run(
            previous_week=data.previous_week,
            feedback=data.feedback,
            goals_update=data.goals_update
        )

        # Return next week to frontend
        return next_week

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )



# @app.post("/full-page")
# async def full_page_endpoint(req: FullPageRequest):
#     if req.mode != "aeo_full":
#         return {"error": "Invalid mode"}
    
#     analysis = await aeo_full_page_analyze(req.text, req.html)
#     return analysis
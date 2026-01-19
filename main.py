from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel
from WorkoutCoach import WorkoutCoach, WorkoutPlansResponse, ProgressionCoach
from uuid import UUID
from Database import update_preferences, upsert_plans, upsert_progression


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


class Input(BaseModel):
    days: int
    goal: str
    train: str
    experience: str
    minutes: int
    week: int = 1

# Instantiate the coach
coach = WorkoutCoach()

@app.post("/agent", response_model=List[WorkoutPlansResponse])
async def run_agent(data: Input):
    """
    Receives frontend input and returns multiple structured workout plans.
    """
    try:
        results = await coach.run(data.days, data.goal, data.train, data.experience, data.minutes, data.week)
        return results
    except Exception as e:
        return {"error": str(e)}
    
class WorkoutPreference(Input):
    pass


class ProgressionInput(BaseModel):
    user_id: UUID

    # The previous week’s workout plan
    previous_plan: dict          # JSON from frontend

    # Input Class Passed
    preference: WorkoutPreference

    # Structured answers (easy for the agent to reason with)
    difficulty: Optional[str] = None
    soreness: Optional[str] = None
    completed: Optional[str] = None
    progression: Optional[str] = None
    day_status: bool

    # Free text (still useful!)
    feedback: Optional[str] = None


progression_agent = ProgressionCoach()

@app.post("/progress", response_model=List[WorkoutPlansResponse])
async def run_progression_agent(data: ProgressionInput):
    try:
        # 1️⃣ Update user preferences if they changed anything
        update_preferences(data.user_id, data.preference)

        # 2️⃣ Save progression answers for this week
        upsert_progression(
            user_id=data.user_id,
            progression_data={
                "difficulty": data.difficulty,
                "soreness": data.soreness,
                "completed": data.completed,
                "progression": data.progression,
                "feedback": data.feedback,
                "day_status": data.day_status
            }
        )

        # 3️⃣ Run AI agent to generate next week's plans
        next_week_plans = await progression_agent.run(
            previous_week=data.previous_plan,
            difficulty=data.difficulty,
            soreness=data.soreness,
            completed=data.completed,
            progression=data.progression,
            feedback=data.feedback,
            day_status=data.day_status
        )

        # 4️⃣ Upsert the existing 3 plans in Supabase
        upsert_plans(data.user_id, next_week_plans)

        # 5️⃣ Return the new plans
        return next_week_plans

    except Exception as e:
        # Optionally raise HTTPException for FastAPI consistency
        raise HTTPException(status_code=500, detail=str(e))




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
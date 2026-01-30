from click import UUID
from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import List, Any, Dict
from pydantic import BaseModel
from WorkoutCoach import WorkoutCoach, WorkoutPlansResponse, ProgressionCoach
from Database import update_preferences, archive_and_update_gym
from Progression import ProgressedWorkoutPlansResponse



load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    location: str
    experience: str
    minutes: int
    week: int = 1

# Instantiate the coach
coach = WorkoutCoach()



@app.post("/agent", response_model=List[WorkoutPlansResponse])
async def run_agent(data: Input):
    try:
        results = await coach.run(
            data.days, data.goal, data.location, data.experience, data.minutes, data.week
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class ProgressionPayload(BaseModel):
    user_id: str
    previous_plan: Dict[str, Any]
    preference: Dict[str, Any]
    difficulty: str
    soreness: str
    completed: str
    progression: str
    feedback: str
    day_status: Dict[str, bool]  



progression_agent = ProgressionCoach()


from fastapi.encoders import jsonable_encoder

@app.post("/progress", response_model=List[ProgressedWorkoutPlansResponse])
async def progress(payload: ProgressionPayload):
    try:
        # 1️⃣ Run the progression agent
        plans = await progression_agent.run(
            previous_week=payload.previous_plan,
            difficulty=payload.difficulty,
            soreness=payload.soreness,
            completed=payload.completed,
            progression=payload.progression,
            feedback=payload.feedback,
            preference=payload.preference,
        )

        # 2️⃣ Increment week BEFORE saving
        current_week = payload.preference.get("week", 1)
        next_week = current_week + 1
        payload.preference["week"] = next_week

        # 3️⃣ Prepare new data to save (convert plans to dict for Supabase)
        new_data = {
            "days": payload.preference.get("days"),
            "goal": payload.preference.get("goal"),
            "location": payload.preference.get("location"),
            "experience": payload.preference.get("experience"),
            "minutes": payload.preference.get("minutes"),
            "difficulty": payload.difficulty,
            "soreness": payload.soreness,
            "completed": payload.completed,
            "progression": payload.progression,
            "feedback": payload.feedback,
            "day_status": payload.day_status,
            "plans": jsonable_encoder(plans),  # ✅ convert to JSON-serializable
        }

        # 4️⃣ Archive current week and save new week
        archive_and_update_gym(UUID(payload.user_id), next_week, new_data)

        # 5️⃣ Return response (FastAPI handles Pydantic serialization)
        return plans

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # auto-restart on code changes
    )




# @app.post("/full-page")
# async def full_page_endpoint(req: FullPageRequest):
#     if req.mode != "aeo_full":
#         return {"error": "Invalid mode"}
    
#     analysis = await aeo_full_page_analyze(req.text, req.html)
#     return analysis
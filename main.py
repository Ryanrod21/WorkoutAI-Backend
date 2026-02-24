from click import UUID
from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import List, Any, Dict
from pydantic import BaseModel
from WorkoutCoach import WorkoutCoach, WorkoutPlansResponse, ProgressionCoach
from Database import delete_user, get_last_week_from_db, archive_and_update_gym, get_history_from_db
from Progression import ProgressedWorkoutPlansResponse



load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://gymai-u2km.onrender.com", "https://iron-path-five.vercel.app",],
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
        last_week = get_last_week_from_db(UUID(payload.user_id))
        next_week = last_week + 1

        history = get_history_from_db(UUID(payload.user_id))
        

        normalized_results = {
            "difficulty": payload.difficulty or 'good',
            "soreness": payload.soreness or 'medium',
            "completed": payload.completed.lower() in ("yes", "partially"),
            "day_status": payload.day_status,
            "preference": payload.preference,
            "feedback": payload.feedback or "Ready to progress safely.",
            "progression": payload.progression or "safe",
        }

        plans = await progression_agent.run(
            previous_week=payload.previous_plan,
            **normalized_results,
            week=next_week,
            history=history,
        )

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
            "plans": jsonable_encoder(plans), 
        }

        archive_and_update_gym(UUID(payload.user_id), next_week, new_data)

        return plans

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/delete_user_data/{user_id}")
async def delete_user_data(user_id: str):
    try:
        result = delete_user(user_id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
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
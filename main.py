from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import List, Any, Dict
from pydantic import BaseModel
from WorkoutCoach import WorkoutCoach, WorkoutPlansResponse, ProgressionCoach
from Database import update_preferences, archive_and_update_gym



load_dotenv()

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "https://gymai-u2km.onrender.com"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
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
    
class WorkoutPreference(Input):
    pass


class ProgressionPayload(BaseModel):
    type: str
    user_id: str
    previous_plan: Dict[str, Any]
    preference: Dict[str, Any]
    difficulty: str
    soreness: str
    completed: bool
    progression: str
    feedback: str
    day_status: Dict[str, Any]


progression_agent = ProgressionCoach()


@app.post("/progress")
async def handle_progress(payload: ProgressionPayload):
    # payload is now a Python dict, not a string
    result = await ProgressionCoach().run(
        previous_week=payload.previous_plan,
        difficulty=payload.difficulty,
        soreness=payload.soreness,
        completed=payload.completed,
        progression=payload.progression,
        feedback=payload.feedback,
    )
    return {"plans": result}





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
from supabase import create_client
from uuid import UUID
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_preferences(user_id: UUID, prefs):
    """
    Upsert the user's gym preferences for week 1
    """
    supabase.table("gym").upsert(
        {
            "user_id": str(user_id),
            "week": 1,  
            "days": prefs.days,
            "goal": prefs.goal,
            "location": prefs.location,
            "experience": prefs.experience,
            "minutes": prefs.minutes
        },
        on_conflict=["user_id", "week"]  # matches your unique constraint
    ).execute()


def archive_and_update_gym(user_id: str, next_week: int, new_data: dict):

    print("UPDATING GYM → user_id:", user_id, "type:", type(user_id))
    print("new_data:", new_data)

    """
    Archives the old gym row for user/week into gym_history,
    then upserts new_data into the gym table.
    """

      # 1️⃣ Fetch current row for this week
    current = supabase.table("gym")\
        .select("*")\
        .eq("user_id", user_id)\
        .execute().data

    
    if current:
        old_row = current[0].copy()
        old_row["archived_at"] = datetime.utcnow().isoformat()
        supabase.table("gym_history").insert(old_row).execute()

            
        supabase.table("gym")\
        .update({**new_data, "week": next_week})\
        .eq("user_id", user_id)\
        .execute()

        
        supabase.table("gym")\
        .update({
            "selected_plan": None,
            "day_status": None
        })\
        .eq("user_id", user_id)\
        .execute()
        
    else:
        print("No existing row found for user_id:", user_id, "week:", next_week )
       
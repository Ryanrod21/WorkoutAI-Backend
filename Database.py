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
        on_conflict=["user_id", "week"]  
    ).execute()



def archive_and_update_gym(user_id: str, next_week: int, new_data: dict):
    
    """
    Archives the old gym row for user/week into gym_history,
    then upserts new_data into the gym table.
    """

      
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
       

def get_last_week_from_db(user_id: UUID) -> int:
    """
    Fetches the last saved week for a given user from the gym table.
    Returns 0 if no previous week is found.
    """
    response = supabase.table("gym").select("week") \
        .eq("user_id", str(user_id)) \
        .order("week", desc=True).limit(1).execute()

    data = response.data
    if data and len(data) > 0:
        return data[0]["week"]
    return 0  

def get_history_from_db(user_id: UUID):
    
    history = supabase.table('gym_history')\
        .select("*")\
        .eq("user_id", user_id)\
        .execute().data
    
    return history if history else None
    
def delete_user(user_id: str):
    """
    Deletes a user from Supabase using the service role key,
    and removes all related rows from gym and gym_history tables.
    WARNING: This permanently removes the user and their data.
    """
    if not user_id:
        print("No user_id provided")
        return {"error": "No user_id provided"}

    try:
        
        supabase.table("gym_history").delete().eq("user_id", user_id).execute()
        supabase.table("gym").delete().eq("user_id", user_id).execute()
   

  
        result = supabase.auth.admin.delete_user(user_id)

        if result.error:
            print("Error deleting user from auth:", result.error)
            return {"error": result.error.message if hasattr(result.error, "message") else str(result.error)}

        print("User and all related data deleted successfully:", user_id)
        return {"success": True}

    except Exception as e:
        print("Error deleting user and data:", e)
        return {"error": str(e)}
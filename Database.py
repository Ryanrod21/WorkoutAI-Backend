from supabase import create_client
import os
from uuid import UUID
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)




def update_preferences(user_id: UUID, prefs):
    # Correct example
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
    on_conflict=["user_id", "week"]).execute()



def archive_and_update_gym(user_id: str, week: int, new_data: dict):
    """
    Archives the old gym row for user/week into gym_history,
    then updates (or inserts) the gym table with new_data.
    """
    # Convert UUID to string if needed
    user_id_str = str(user_id)

    # 1️⃣ Fetch current row
    current = supabase.table("gym").select("*")\
        .eq("user_id", user_id_str)\
        .eq("week", week).execute().data

    if current:
        old_row = current[0].copy()
        old_row["archived_at"] = datetime.utcnow().isoformat()

        # 2️⃣ Insert old row into history
        supabase.table("gym_history").insert(old_row).execute()

    # 3️⃣ Upsert new data into gym
    supabase.table("gym").upsert(
        {
            "user_id": user_id_str,
            "week": week,
            **new_data
        },
        on_conflict=["user_id", "week"]  # ⚡ Must be the UNIQUE columns, not constraint name
    ).execute()


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
            "week": 1,  # always week 1 for preferences
            "days": prefs.days,
            "goal": prefs.goal,
            "location": prefs.location,
            "experience": prefs.experience,
            "minutes": prefs.minutes
        },
        on_conflict=["user_id", "week"]  # matches your unique constraint
    ).execute()


def archive_and_update_gym(user_id: UUID, week: int, new_data: dict):
    """
    Archives the old gym row for user/week into gym_history,
    then upserts new_data into the gym table.
    """
    user_id_str = str(user_id)  # ✅ Convert UUID to string for Supabase
    week_int = int(week)        # ✅ Ensure week is integer

    # 1️⃣ Fetch current row for this user/week
    current = supabase.table("gym")\
        .select("*")\
        .eq("user_id", user_id_str)\
        .eq("week", week_int)\
        .execute().data

    # 2️⃣ Archive old row if exists
    if current:
        old_row = current[0].copy()
        old_row["archived_at"] = datetime.utcnow().isoformat()
        supabase.table("gym_history").insert(old_row).execute()

    # 3️⃣ Upsert new data
    supabase.table("gym").upsert(
        {
            "user_id": user_id_str,
            "week": week_int,
            **new_data
        },
        on_conflict=["week", "user_id"]  # ✅ Must match the unique constraint
    ).execute()

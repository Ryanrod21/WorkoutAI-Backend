from supabase import create_client
import os
from uuid import UUID
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)




def update_preferences(user_id: UUID, prefs):
    supabase.table("gym").upsert({
        "user_id": str(user_id),
        "days": prefs.days,
        "goal": prefs.goal,
        "location": prefs.location,
        "experience": prefs.experience,
        "minutes": prefs.minutes
    }, on_conflict="gym_user_week_unique").execute()


def archive_and_update_gym(user_id: UUID, week: int, new_data: dict):
    # Convert UUID to string
    user_id_str = str(user_id)

    # 1️⃣ Remove any accidental duplicates first
    all_rows = supabase.table("gym").select("*")\
        .eq("user_id", user_id_str)\
        .eq("week", week).execute().data
    if len(all_rows) > 1:
        # Keep only the first, archive the rest
        for row in all_rows[1:]:
            row["archived_at"] = datetime.utcnow().isoformat()
            supabase.table("gym_history").insert(row).execute()
            supabase.table("gym").delete().eq("id", row["id"]).execute()

    # 2️⃣ Archive the current row if exists
    if all_rows:
        old_row = all_rows[0].copy()
        old_row["archived_at"] = datetime.utcnow().isoformat()
        supabase.table("gym_history").insert(old_row).execute()

    # 3️⃣ Upsert new data
    supabase.table("gym").upsert({
        "user_id": user_id_str,
        "week": week,
        **new_data
    }, on_conflict="gym_user_week_unique").execute()


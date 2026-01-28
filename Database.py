from supabase import create_client
import os
from uuid import UUID
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_preferences(user_id: UUID, prefs):
    """
    Upsert questionnaire answers for WEEK 1
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
        on_conflict=["week", "user_id"]
    ).execute()


def archive_and_update_gym(user_id: UUID, week: int, new_data: dict):
    """
    Archive current row (if exists) then upsert new data into gym table.
    Handles both old gym data and new progression fields like:
    - plans
    - day_status
    - progression_notes
    """
    user_id_str = str(user_id)

    # Fetch existing row
    current = (
        supabase.table("gym")
        .select("*")
        .eq("user_id", user_id_str)
        .eq("week", week)
        .execute()
        .data
    )

    # Archive if exists
    if current:
        old_row = current[0].copy()
        old_row.pop("id", None)  # Remove primary key to avoid conflicts
        old_row["archived_at"] = datetime.utcnow().isoformat()

        supabase.table("gym_history").insert(old_row).execute()

    # Upsert new data (merge old gym fields + new progression data)
    upsert_payload = {
        "user_id": user_id_str,
        "week": week,
        **new_data  # new_data can include old fields + progression fields
    }

    supabase.table("gym").upsert(upsert_payload).execute()

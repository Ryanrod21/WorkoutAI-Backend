from supabase import create_client
import os
from uuid import UUID


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_preferences(user_id: UUID, prefs):
    """
    Update user preferences in the gym table.
    prefs is expected to be a WorkoutPreference-like object
    """
    supabase.table("gym").upsert({
        "user_id": str(user_id),
        "days": prefs.days,
        "goal": prefs.goal,
        "train": prefs.train,
        "experience": prefs.experience,
        "minutes": prefs.minutes
    }, on_conflict=["user_id"]).execute()


def get_next_week_number(user_id: UUID) -> int:
    """
    Fetch last saved week for this user and return next week number
    """
    result = supabase.table("gym") \
        .select("week") \
        .eq("user_id", str(user_id)) \
        .order("week", desc=True) \
        .limit(1) \
        .execute()
    
    last_week = result.data[0]["week"] if result.data else 0
    return last_week + 1


def upsert_plans(user_id: UUID, new_plans: list):
    """
    Insert or update 3 new plans for a user for the next week.
    Returns the week number used.
    """
    week = get_next_week_number(user_id)

    supabase.table("gym").upsert({
        "user_id": str(user_id),
        "week": week,
        "plans": new_plans  # JSON array of plans
    }, on_conflict=["user_id", "week"]).execute()

    return week


def upsert_progression(user_id: UUID, week: int, progression_data: dict):
    """
    Insert or update progression answers for a specific week
    """
    supabase.table("progression").upsert({
        "user_id": str(user_id),
        "week": week,
        "difficulty": progression_data.get("difficulty"),
        "soreness": progression_data.get("soreness"),
        "completed": progression_data.get("completed"),
        "progression": progression_data.get("progression"),
        "feedback": progression_data.get("feedback")
    }, on_conflict=["user_id", "week"]).execute()
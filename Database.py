from supabase import create_client
import os

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_preferences(user_id, prefs):
    """
    Update user preferences: days, goal, train, experience, minutes
    """
    supabase.table("gym").upsert({
        "user_id": str(user_id),
        "days": prefs.days,
        "goal": prefs.goal,
        "train": prefs.train,
        "experience": prefs.experience,
        "minutes": prefs.minutes
    }, on_conflict=["user_id"]).execute()


def update_plans(user_id, new_plans):
    """
    Replace the existing 3 plans for a user with the new ones.
    """
    supabase.table("gym").update({
        "plans": new_plans  # store as JSON array
    }).eq("user_id", str(user_id)).execute()


def upsert_progression(user_id, progression_data):
    """
    Insert or update progression answers for a specific week.
    """
    supabase.table("progression").upsert({
        "user_id": str(user_id),
        "difficulty": progression_data.get("difficulty"),
        "soreness": progression_data.get("soreness"),
        "completed": progression_data.get("completed"),
        "progression": progression_data.get("progression"),
        "feedback": progression_data.get("feedback")
    }, on_conflict=["user_id", "week"]).execute()

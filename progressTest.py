from uuid import UUID , uuid4
from datetime import datetime
from Database import archive_and_update_gym, supabase  # change your_backend_module to your .py file name

# # Test data
# test_user_id = UUID("bcfacdec-5009-4caf-82a9-471c3c9b187f")
# test_week = 1
# new_data = {
#     "difficulty": "medium",
#     "soreness": "some",
#     "completed": "Yes",
#     "progression": "good",
#     "feedback": "Felt strong this week"
# }

# # Run archive & update
# archive_and_update_gym(user_id=test_user_id, week=test_week, new_data=new_data)

# # Fetch to see results
# current = supabase.table("gym").select("*").eq("user_id", str(test_user_id)).eq("week", test_week).execute().data
# print("Current gym row:", current)

# history = supabase.table("gym_history").select("*").eq("user_id", str(test_user_id)).execute().data
# print("History rows:", history)

test_user_id = uuid4()
test_week = 1
new_data = {"difficulty": "Easy", "soreness": "Not sore", "completed": "Yes"}

archive_and_update_gym(user_id=test_user_id, week=test_week, new_data=new_data)
print("Upsert successful!")

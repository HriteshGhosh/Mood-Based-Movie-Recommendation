import pandas as pd

from logic.user_manager import get_or_create_user_id
from model.hybrid import hybrid_recommendation

# Load prepared datasets
movies = pd.read_csv("data/tmdb_movies.csv")
movies = movies.sample(n=10000)
interactions = pd.read_csv("data/user_interactions.csv")

# User input (terminal)
try:
    username = input("Enter username: ").strip()
    mood = input(
        "Enter mood (happy 😊 / sad 😢 / chill 😎 / excited 😃 / dark 😶‍🌫️): "
    ).strip().lower()
    user_age = int(input("Enter your age: "))
except ValueError:
    print("❌ Invalid input. Please enter correct values.")
    exit()

# Get or create user ID
user_id = get_or_create_user_id(username)
print(f"\nLogged in as '{username}' (user_id = {user_id})")

# Generate Hybrid Recommendations
recommendations = hybrid_recommendation(
    user_id=user_id,
    user_interactions=interactions,
    movies=movies,
    mood=mood,
    user_age=user_age,
    top_n=5
)

# Output
print("\n🎬 Movie Recommendations:")
print(recommendations.to_string(index=False))

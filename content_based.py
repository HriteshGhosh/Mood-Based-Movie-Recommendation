import pandas as pd
import ast

from logic.mood_mapper import get_mood_genre_weights
from logic.age_filter import apply_age_and_content_filter


def extract_genres(genre_str):
    if pd.isna(genre_str):
        return []
    try:
        return [g["name"] for g in ast.literal_eval(genre_str)]
    except:
        return []


def recommend_movies(
    user_id,              # kept for interface consistency
    user_interactions,    # not used here (by design)
    movies,
    mood,
    user_age,
    top_n=5
):
    # ---- Filter movies ----
    movies = apply_age_and_content_filter(
        movies,
        user_age=user_age
    )

    mood_weights = get_mood_genre_weights(mood)
    scores = []

    for _, row in movies.iterrows():
        genres = extract_genres(row["genres"])
        score = 0

        # Mood-based genre boost
        for genre in genres:
            score += mood_weights.get(genre, 1)*2.5

        # Quality & popularity boost
        score += row["vote_average"] * 0.05
        score += row["popularity"] * 0.002

        scores.append(score)

    movies = movies.copy()
    movies["content_score"] = scores

    return movies.sort_values(
        "content_score",
        ascending=False
    ).head(top_n)[["id", "title", "content_score"]]

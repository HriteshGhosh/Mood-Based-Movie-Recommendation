import pandas as pd
import ast


def extract_genres(genre_str):
    if pd.isna(genre_str):
        return []
    try:
        return [g["name"] for g in ast.literal_eval(genre_str)]
    except:
        return []


def apply_age_and_content_filter(
    movies_df,
    user_age,
    allow_adult=False,
    allow_horror=True,
    allow_violence=True
):
    filtered = []

    for _, row in movies_df.iterrows():
        genres = extract_genres(row["genres"])

        # Age filter
        if user_age < 18 and any(
            g in genres for g in ["Horror", "Crime", "Thriller"]
        ):
            continue

        # Content sensitivity
        if not allow_horror and "Horror" in genres:
            continue

        if not allow_violence and any(
            g in genres for g in ["Action", "War"]
        ):
            continue

        # TMDB adult flag
        if not allow_adult and row.get("adult", False):
            continue

        filtered.append(row)

    return pd.DataFrame(filtered)

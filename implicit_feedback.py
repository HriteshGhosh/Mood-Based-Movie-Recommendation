import pandas as pd

def build_user_interactions():
    # Load datasets
    ratings = pd.read_csv("data/ratings.csv")
    implicit = pd.read_csv("data/implicit_feedback.csv")

    # Aggregate implicit feedback per user-movie
    implicit_agg = implicit.groupby(
        ["user_id", "movie_id"],
        as_index=False
    )["implicit_score"].sum()

    # Merge explicit + implicit
    interactions = pd.merge(
        ratings,
        implicit_agg,
        on=["user_id", "movie_id"],
        how="left"
    )

    # Fill missing implicit scores
    interactions["implicit_score"] = interactions["implicit_score"].fillna(0)

    # Final interaction score
    interactions["final_score"] = (
        interactions["rating"] + 0.3 * interactions["implicit_score"]
    )

    # Save
    interactions.to_csv("data/user_interactions.csv", index=False)

    print("user_interactions.csv created successfully")

    return interactions


# Allow standalone run
if __name__ == "__main__":
    build_user_interactions()

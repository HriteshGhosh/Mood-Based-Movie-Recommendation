import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def recommend_movies_cf(
    user_id,
    interactions_df,
    movies_df,
    top_n=10
):
    """
    User-User Collaborative Filtering using cosine similarity
    """

    # Create user-movie matrix
    user_movie = interactions_df.pivot_table(
        index="user_id",
        columns="movie_id",
        values="final_score",
        fill_value=0
    )

    # Check if user exists
    if user_id not in user_movie.index:
        return pd.DataFrame(columns=["movie_id", "title", "cf_score"])

    # Compute similarity matrix
    similarity = cosine_similarity(user_movie)
    sim_df = pd.DataFrame(
        similarity,
        index=user_movie.index,
        columns=user_movie.index
    )

    # Get similar users
    similar_users = (
        sim_df[user_id]
        .sort_values(ascending=False)
        .drop(user_id)
        .head(10)
        .index
    )

    # Aggregate scores from similar users
    user_scores = (
        user_movie.loc[similar_users]
        .mean()
        .sort_values(ascending=False)
    )

    # Remove already watched movies
    watched = set(
        interactions_df[
            interactions_df["user_id"] == user_id
        ]["movie_id"]
    )

    recommendations = user_scores.drop(labels=watched, errors="ignore")

    # Prepare output
    recs = (
        recommendations
        .head(top_n)
        .reset_index()
        .rename(columns={0: "cf_score"})
    )

    return recs.merge(
        movies_df,
        on="movie_id"
    )[["movie_id", "title", "cf_score"]]

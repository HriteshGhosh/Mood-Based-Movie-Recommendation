import pandas as pd
from model.content_based import recommend_movies
from model.collaborative import recommend_movies_cf


def hybrid_recommendation(
    user_id,
    user_interactions,
    movies,
    mood,
    user_age,
    top_n=5,
    w_content=0.7,
    w_cf=0.3
):
    # Content-based (TMDB)
    content_recs = recommend_movies(
        user_id=user_id,
        user_interactions=user_interactions,
        movies=movies,
        mood=mood,
        user_age=user_age,
        top_n=top_n * 3
    )

    # Collaborative (MovieLens only)
    cf_recs = recommend_movies_cf(
        user_id=user_id,
        interactions_df=user_interactions,
        movies_df=movies.rename(columns={"id": "movie_id"}),
        top_n=top_n * 3
    )

    hybrid = pd.merge(
        content_recs,
        cf_recs,
        left_on="id",
        right_on="movie_id",
        how="outer"
    ).fillna(0).infer_objects(copy=False)

    # Normalize
    if hybrid["content_score"].max() > 0:
        hybrid["content_score"] /= hybrid["content_score"].max()
    if hybrid["cf_score"].max() > 0:
        hybrid["cf_score"] /= hybrid["cf_score"].max()

    hybrid["hybrid_score"] = (
        w_content * hybrid["content_score"] +
        w_cf * hybrid["cf_score"]
    )

    return hybrid.sort_values(
    "hybrid_score",
    ascending=False
).head(top_n)[["title_x"]].rename(
    columns={"title_x": "title"}
)

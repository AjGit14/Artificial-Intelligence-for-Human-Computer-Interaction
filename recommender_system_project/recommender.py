import os
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.csv")
MOVIES_FILE = os.path.join(DATA_DIR, "movies.csv")

# Load data
if not (os.path.exists(RATINGS_FILE) and os.path.exists(MOVIES_FILE)):
    raise FileNotFoundError(
        "ratings.csv and movies.csv were not found in the data/ directory.\n"
        "Download the MovieLens 100K (or similar) dataset and place ratings.csv and movies.csv into data/."
    )

ratings_df = pd.read_csv(RATINGS_FILE)
movies_df = pd.read_csv(MOVIES_FILE)

# Keep only necessary columns
ratings_df = ratings_df[["userId", "movieId", "rating"]]

reader = Reader(rating_scale=(ratings_df["rating"].min(), ratings_df["rating"].max()))
data = Dataset.load_from_df(ratings_df.rename(columns={"userId": "user", "movieId": "item"}), reader)

# Train-test split just for basic evaluation; then retrain on full data
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

algo = SVD()
algo.fit(trainset)

# Evaluate (optional; could be logged)
# from surprise import accuracy
# predictions = algo.test(testset)
# print("Test RMSE:", accuracy.rmse(predictions, verbose=True))

# Retrain on full data for production use
full_trainset = data.build_full_trainset()
algo.fit(full_trainset)

# Pre-compute basic popularity info
movie_stats = ratings_df.groupby("movieId")["rating"].agg(["count", "mean"]).reset_index()
movie_stats = movie_stats.merge(movies_df[["movieId", "title"]], on="movieId", how="left")


def get_popular_movies(n=10, min_ratings=50):
    """Return a list of popular movies with at least min_ratings ratings."""
    popular = movie_stats[movie_stats["count"] >= min_ratings].copy()
    if popular.empty:
        # Fallback: ignore min_ratings if dataset is small
        popular = movie_stats.copy()
    popular = popular.sort_values(by=["mean", "count"], ascending=[False, False]).head(n)
    # Convert to list of dicts for easier use in templates
    movies = []
    for _, row in popular.iterrows():
        movies.append(
            {
                "movie_id": str(row["movieId"]),
                "title": row["title"],
                "avg_rating": round(row["mean"], 2),
                "rating_count": int(row["count"]),
            }
        )
    return movies


def get_top_n_recommendations(user_id, n=10):
    """Generate top-N recommendations for a given user_id using the trained SVD model.

    If user_id was not in the training data, Surprise will fall back to a
    global-baseline style estimate. This is sufficient for a simple demo.
    """
    # All unique movie IDs
    all_movie_ids = ratings_df["movieId"].unique()

    # Movies the user has already rated
    rated_movie_ids = ratings_df[ratings_df["userId"] == int(user_id)]["movieId"].unique()             if str(user_id).isdigit() and int(user_id) in set(ratings_df["userId"].unique()) else []

    candidates = [mid for mid in all_movie_ids if mid not in rated_movie_ids]

    predictions = []
    for mid in candidates:
        pred = algo.predict(str(user_id), str(mid))
        predictions.append((mid, pred.est))

    # Sort by estimated rating
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_n = predictions[:n]

    # Join with movie metadata
    movie_meta = movies_df.set_index("movieId")
    results = []
    for mid, est in top_n:
        title = movie_meta.loc[mid, "title"] if mid in movie_meta.index else f"Movie {mid}"
        results.append(
            {
                "movie_id": str(mid),
                "title": title,
                "pred_rating": round(est, 2),
                "explanation": "Recommended based on similar users' preferences.",
            }
        )
    return results

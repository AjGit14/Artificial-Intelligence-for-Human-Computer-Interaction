from flask import Flask, render_template, request, redirect, url_for
from recommender import get_top_n_recommendations, get_popular_movies

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()
        if not user_id:
            error = "Please enter a user ID (e.g., 1–610 for MovieLens 100K)."
            return render_template("index.html", error=error)
        return redirect(url_for("rate", user_id=user_id))
    return render_template("index.html")


@app.route("/rate/<user_id>", methods=["GET", "POST"])
def rate(user_id):
    popular_movies = get_popular_movies(n=10)
    if request.method == "POST":
        # In this minimal prototype we simply read ratings
        # and could log them to a file for later analysis.
        ratings = {}
        for movie_id in request.form:
            if movie_id.startswith("movie_"):
                mid = movie_id.split("_", 1)[1]
                value = request.form[movie_id]
                if value:
                    try:
                        ratings[mid] = float(value)
                    except ValueError:
                        continue
        # TODO: extend the recommender to incorporate these ratings.
        # For now, we ignore them and move on to recommendations.
        return redirect(url_for("recommend", user_id=user_id))
    return render_template("rate.html", user_id=user_id, movies=popular_movies)


@app.route("/recommend/<user_id>")
def recommend(user_id):
    recommendations = get_top_n_recommendations(user_id=user_id, n=10)
    return render_template("recommend.html", user_id=user_id, recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)

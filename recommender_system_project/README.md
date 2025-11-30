# Movie Recommendation System (AI/HCI Project)

This is a minimal example of a movie recommendation system built with:

- Python
- Flask (for the web interface)
- Surprise (for the recommendation algorithm)
- MovieLens-style ratings and movies data

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the MovieLens dataset (e.g., MovieLens 100K) from GroupLens and place
   `ratings.csv` and `movies.csv` into the `data/` directory.

4. Run the app:

   ```bash
   python app.py
   ```

5. Open a browser at `http://127.0.0.1:5000/` and try user IDs such as 1–610.

## Notes

- This project is intentionally simple and meant as a starting point for your
  course assignment. You are expected to extend it, document your changes,
  and describe your experience in your APA-formatted report.
- Be sure to credit any external tutorials or examples you use as inspiration.

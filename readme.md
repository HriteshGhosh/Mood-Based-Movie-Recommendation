# Mood-Based Movie Recommender

A **hybrid movie recommendation system** that suggests movies based on a user’s **mood**, **age**, and **interaction history**, built using **Python**, **Pandas**, and **Streamlit**, with modern movie data from **TMDB**.

---

##  Features

-  Mood-based recommendations (Happy, Sad, Chill, Excited, Dark)
-  Hybrid recommendation system  
  - Content-based (TMDB metadata)
  - Collaborative filtering (MovieLens interactions)
-  Username-based user management
-  Age & content sensitivity filtering
-  Modern Streamlit UI (Prussian blue theme)
-  One-click copy button for movie titles
-  Choose number of recommendations (1–10)
-  Fast and lightweight (no heavy ML libraries)

---

## Tech Stack

- **Python 3.9+**
- **Streamlit** – UI
- **Pandas** – Data processing
- **NumPy** – Scoring & randomness
- **TMDB Dataset** – Modern movie data
- **MovieLens Dataset** – User interactions

---

## Project Structure
Movie_recommender/
│
├── app.py                     # Streamlit UI
├── main.py                    # CLI version (optional)
├── requirements.txt
├── README.md
│
├── data/
│   ├── tmdb_movies.csv        # Cleaned TMDB dataset
│   ├── user_interactions.csv # Interaction data
│   └── users.csv              # Username → user_id mapping
│
├── logic/
│   ├── age_filter.py
│   ├── mood_mapper.py
│   └── user_manager.py
│
├── model/
│   ├── content_based.py
│   ├── collaborative.py
│   └── hybrid.py

## Install Dependencies
pip install -r requirements.txt

## Run the streamlit app
streamlit run app.py
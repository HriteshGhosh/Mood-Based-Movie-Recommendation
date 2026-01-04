import streamlit as st
import pandas as pd

from logic.user_manager import get_or_create_user_id
from model.hybrid import hybrid_recommendation

# Page config
st.set_page_config(
    page_title="Mood-Based Movie Recommender 🎬",
    page_icon="🎬",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b3c5d, #082f47);
    }

    h1, h2, h3, h4, h5, h6,
    p, span, label, div {
        color: #ffffff !important;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSlider label,
    .stRadio label {
        color: #ffffff !important;
        font-weight: 600;
    }

    .stRadio div {
        color: #ffffff !important;
        font-size: 16px;
    }

    div.stButton > button {
        background-color: #1f6feb;
        color: #ffffff !important;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-size: 16px;
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #174ea6;
        transform: scale(1.03);
    }

    div.stButton > button:active {
        background-color: #0b3d91;
        transform: scale(0.97);
    }

    div[data-testid="stAlert"] {
        background-color: #113f67;
        border-left: 5px solid #1f6feb;
        color: #ffffff !important;
    }

    .recommend-card {
        background-color: #0f3f63;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-weight: 500;
    }

    .copy-btn {
        background: #1f6feb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 10px;
        cursor: pointer;
    }

    .copy-btn:hover {
        background: #174ea6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🎬 Mood-Based Movie Recommender")

# Load data (cached, NO randomness here)
@st.cache_data
def load_data():
    movies = pd.read_csv("data/tmdb_movies.csv")
    interactions = pd.read_csv("data/user_interactions.csv")
    return movies, interactions


movies, interactions = load_data()

# Layout
left, right = st.columns([1, 1.4])

# LEFT: User input
with left:
    st.subheader("👤 User Details")

    username = st.text_input(
        "Username",
        placeholder="e.g. hritesh_01"
    )

    user_age = st.number_input(
        "Your age",
        min_value=1,
        max_value=100,
        value=18
    )

    st.subheader("🎭 Select your mood")

    mood_map = {
        "😊 Happy": "happy",
        "😢 Sad": "sad",
        "😎 Chill": "chill",
        "😃 Excited": "excited",
        "😶‍🌫️ Dark": "dark"
    }

    mood_label = st.radio(
        "",
        list(mood_map.keys())
    )

    mood = mood_map[mood_label]

    st.subheader("🔢 Number of recommendations")
    top_n = st.slider(
        "Choose how many movies you want",
        min_value=1,
        max_value=10,
        value=5
    )

    recommend_clicked = st.button("🎥 Recommend Movies")

# RIGHT: Recommendations
with right:
    st.subheader("🍿 Recommendations")

    if recommend_clicked:
        if not username:
            st.warning("Please enter a username.")
        else:
            user_id = get_or_create_user_id(username)

            st.info(
                f"Logged in as **{username}**  \n"
                f"Mood: **{mood_label}**  \n"
                f"Age: **{user_age}**"
            )

            # IMPORTANT: sample AFTER click (no cache freezing)
            movies_sampled = movies.sample(n=5000)

            recs = hybrid_recommendation(
                user_id=user_id,
                user_interactions=interactions,
                movies=movies_sampled,
                mood=mood,
                user_age=user_age,
                top_n=top_n
            )

            st.markdown("### 🎬 Title")

            for _, row in recs.iterrows():
                col_title, col_copy = st.columns([0.88, 0.12])

                with col_title:
                    st.markdown(
                        f"""
                        <div class="recommend-card">
                            {row["title"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col_copy:
                    st.markdown(
                        f"""
                        <button class="copy-btn"
                        onclick="navigator.clipboard.writeText('{row['title']}')">
                        📋
                        </button>
                        """,
                        unsafe_allow_html=True
                    )

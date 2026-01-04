# logic/mood_mapper.py

def get_mood_genre_weights(mood):
    """
    Returns genre weight boosts based on user mood
    """

    mood = mood.lower()

    mood_map = {
        "happy": {
            "Comedy": 1.8,
            "Animation": 1.8,
            "Children": 1.3
        },
        "sad": {
            "Drama": 2.0,
            "Romance": 1.4,
            "music": 1.8
        },
        "chill": {
            "Drama": 1.3,
            "Romance": 1.2,
            "Adventure": 1.5
        },
        "excited": {
            "Action": 1.5,
            "Thriller": 1.4,
            "Sci-Fi": 1.3
        },
        "dark": {
            "Crime": 1.9,
            "Horror": 1.8,
            "Mystery": 1.5
        }
    }

    return mood_map.get(mood, {})

import pandas as pd
import os

USER_FILE = "data/users.csv"
START_USER_ID = 944  # after MovieLens users


def get_or_create_user_id(username):
    # Create file if not exists
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "user_id"])
        df.to_csv(USER_FILE, index=False)

    users = pd.read_csv(USER_FILE)

    # Existing user
    if username in users["username"].values:
        return int(users[users["username"] == username]["user_id"].iloc[0])

    # New user
    if users.empty:
        new_id = START_USER_ID
    else:
        new_id = users["user_id"].max() + 1

    users.loc[len(users)] = [username, new_id]
    users.to_csv(USER_FILE, index=False)

    return int(new_id)

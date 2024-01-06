# high_score.py
import os

HIGH_SCORE_FILE = "high_score.txt"


def get_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as file:
        score = file.read()
    return int(score) if score.isdigit() else 0


def save_high_score(new_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_score))


def update_high_score(player_score):
    high_score = get_high_score()
    if player_score > high_score:
        save_high_score(player_score)
        return True
    return False

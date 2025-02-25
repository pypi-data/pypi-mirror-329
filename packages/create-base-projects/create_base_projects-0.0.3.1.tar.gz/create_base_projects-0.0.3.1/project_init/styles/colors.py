from random import randint

COLORS = ["green", "blue", "yellow", "cyan", "purple", "orange", "lime"]

def get_random_color() -> str:
    return COLORS[randint(0, len(COLORS) - 1)]


import random
import json
from website.paths.paths import cernabila_getword_path

def get_word() -> str:
    with open(cernabila_getword_path()) as file:
        file = json.load(file)
        return random.choice(file)

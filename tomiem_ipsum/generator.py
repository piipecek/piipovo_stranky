import random
from pathlib import Path
from website.paths.paths import tomiem_result_path

def get_tomiem(words:  int) -> str:
    result = "Tomiem ipsum dolor sit amet. "
    with open(tomiem_result_path()) as file:
        file = file.read().split("\n")

    zacatek = random.randint(0,len(file)+1)

    while (len(result.split(" ")) <= words):
        result += file[zacatek]
        zacatek += 1
    result = result.split(" ")[:words]
    
    return " ".join(result)

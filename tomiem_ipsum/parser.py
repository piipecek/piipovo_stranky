from pathlib import Path
import csv

"""
Projde texťáky ze složky raw a vybere promluvy Tomia Okamury.
"""

raw_path = Path.cwd() / "raw"
result_path = Path.cwd() / "result.txt"

# with open("poslanci.txt") as poslanci:
#     poslanci = poslanci.read().split("\n")

result = []
for raw_file in raw_path.iterdir():
    if raw_file.name == ".DS_Store":
        continue

    with open(raw_file) as file:
        file = csv.reader(file)
        for line in file:
            if line[7] == "Tomio Okamura":
                result.append(line[13])

with open(result_path, "w") as result_file:
    result = list(set(result))
    joined = "\n".join(result)
    joined = joined.replace("\n\n", "\n")
    joined = joined.replace("Neautorizováno !\n", "")
    joined = joined.replace("Neprošlo jazykovou korekturou, neautorizováno !\n", "")
    joined = joined.replace("***", "")
    result_file.write(joined)


def pretty_date(date: str) -> str:
    date, time = date.split(" ")
    year, month, day = date.split("-")
    time, milis = time.split(".")
    hour, minute, sec = time.split(":")
    return f"{day}. {month}. {year}, {hour}:{minute}:{sec}"
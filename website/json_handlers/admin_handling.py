from website.paths.paths import admins_path


def is_admin(email: str) -> bool:
    with open(admins_path()) as file:
        admins = file.read().split("\n")
        if email in admins:
            return True
        return False
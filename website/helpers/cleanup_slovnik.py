from website.models.slovnik import Slovnik

def cleanup_slovnik():
    s = Slovnik()
    for word in s.slovicka:
        word.czech = list(filter(lambda x: x != "-", word.czech))
        word.english = list(filter(lambda x: x != "-", word.english))
        word.german = list(filter(lambda x: x != "-", word.german))
        word.druh = list(filter(lambda x: x != "-", word.druh))
        word.kategorie = list(filter(lambda x: x != "-", word.kategorie))
        word.asociace = list(filter(lambda x: x != "-", word.asociace))
    s.ulozit_do_db()
        

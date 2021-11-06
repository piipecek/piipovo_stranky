from website.models.slovnik import Slovnik
from website.models.settings import Settings

def cleanup_slovnik() -> None:
    s = Slovnik.get()
    for word in s.slovicka:
        def _cleanup_slovo(slovo: list) -> list:
            if "" in slovo:
                slovo.remove("")
            if "-" in slovo:
                slovo.remove("-")
            return slovo
        for jazyk in Settings.get().data["jazyky"]:
            word.v_jazyce[jazyk] = _cleanup_slovo(word.v_jazyce[jazyk])    
        word.druh = _cleanup_slovo(word.druh)
        word.kategorie = _cleanup_slovo(word.kategorie)
        word.asociace = _cleanup_slovo(word.asociace)
    s.ulozit_do_db()
        

# STL-TO-PRINT

už se to rozbíhá

## Hosting

- používám hosting na [python anywhere](https://eu.pythonanywhere.com).
- přístupová data mám a můžu je poskytnout, ale hlavní je, že kód je zde na githubu

## Struktura a styl

- Složky jsou strukturovány tak, jak mě to naučili v [tomhle videu v tomhle čase](https://youtu.be/dam0GPOAvVI?t=275)
- Při programování byl používán [PEP 8](https://www.python.org/dev/peps/pep-0008/) styl pro formátování python kódu.
- Komentáře v kódu často vedou k nepřesnostem. Zastarávají a stávají se irelevantními. V případě Pythonu se správně napsaný kód dá číst (s trochou nadsázky) jako kniha. O to se také snažím, tedy dokumentace v kódu místo nemá. Jedinou výjimou jsou TypeHints, které v kódu pomáhají mimojiné nahlédnout na typ proměnných.
- Řada souborů se sama vytváří při spuštění a nejsou součástí version control. Jsou to:
  - known_bugs.json
  - website/database.db
  - user_data

## Použité knihovny

- instalované přes pip
  - [Flask](https://flask.palletsprojects.com/en/2.0.x/) - framework pro web development
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - extension Flasku pro práci s databázemi
  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - extension flasku pro podporu přihlašování userů
- součástí standard library:
  - [json](https://docs.python.org/3/library/json.html) - pomáhá správně zapisovat dict proměnné do souborů
  - [typing](https://docs.python.org/3/library/typing.html) - pomáhá mít pořádek v typech proměnných nebo třeba v return values funkcí
  - [pathlib](https://docs.python.org/3/library/pathlib.html) - lepší práce s cestami k souborům než jen "/path/to/file". Hlavně má zaručit funkčnost na různých OS.

## Local build

bohužel neumím přesně syntax příkazů, tak to popíšu slovy:

Pro spuštění flask serveru je potřeba

- mít local verzi tohoto repa
- mít naistalovaný Python a pip
- pomocí pip instalovat všechny knihovny v requirements.txt
- spustit skript main.py

## Pro přístě

- pro správné nastavení Python anywhere WSGI aplikace doporučuju [tohle video](https://youtu.be/5jbdkOlf4cY)
- na [tomhle čase](https://youtu.be/dam0GPOAvVI?t=4367) mě naučili login support

creating requirements.txt: pipenv run pip freeze > requirements.txt
import Cookies from "./js.cookie.mjs"
import httpGet from "./httpGet.js"
let names_to_translate =  ["nadpis", "myslenka_o_multilang", "name_neprislo", "nenasel_jazyk"]

let cs_button = document.getElementById("cs")
let en_button = document.getElementById("en")

cs_button.addEventListener("click", function() {zmen_cookie("cs")})
en_button.addEventListener("click", function() {zmen_cookie("en")})

function zmen_cookie(jazyk) {
    Cookies.set("jazyk", jazyk)
    zmen_jazyk()
}

function zmen_jazyk() {
    if (Cookies.get("jazyk")) {
        let jazyk = Cookies.get("jazyk")
        let multilang_soubor = JSON.parse(httpGet("/send_multilang/"+jazyk+"/jazykova_mutace"))
        for (let id of names_to_translate) {
            let preklad = "Ze serveru nepřišel překlad pro tohle name: " + id + ". Nejspíše je špatně definovaný záznam v multilang souboru."
            for (let zaznam of multilang_soubor) {
                if (zaznam["name"] == id) {
                    preklad = zaznam["preklad"]
                    break
                }
            }
            document.getElementById(id).innerHTML = preklad
        }
        
    } else {
        Cookies.set("jazyk", "cs") // default
        zmen_jazyk()
    }
}

zmen_jazyk() // pri prvnim nacteni stranky to defaaultne nekam - treba na cs
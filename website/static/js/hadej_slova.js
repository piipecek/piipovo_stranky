function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
let db = JSON.parse(httpGet("/visuals/hadej_slova_getter"))
let slova = [] //sem se ukládaj slova, která si uživatel vybral
let dbs = [db] // sem se ukládaj databáze po jednotlivejch krocích
let temp_db = [] //se mse ukládá jednotlivej krok
let cetnosti = {
    "a": 6.2193,
    "\u00e1": 2.2355,
    "b": 1.5582,
    "c": 1.6067,
    "\u010d": 0.949,
    "d": 3.6019,
    "\u010f": 0.0222,
    "e": 7.6952,
    "\u00e9": 1.3346,
    "\u011b": 1.6453,
    "f": 0.2732,
    "g": 0.2729,
    "h": 1.2712,
    "i": 4.3528,
    "\u00ed": 3.2699,
    "j": 2.1194,
    "k": 3.7367,
    "l": 3.8424,
    "m": 3.2267,
    "n": 6.5353,
    "\u0148": 0.0814,
    "o": 8.6664,
    "\u00f3": 0.0313,
    "p": 3.4127,
    "q": 0.0013,
    "r": 3.697,
    "\u0159": 1.2166,
    "s": 4.516,
    "\u0161": 0.8052,
    "t": 5.7268,
    "\u0165": 0.0426,
    "u": 3.1443,
    "\u00fa": 0.1031,
    "\u016f": 0.6948,
    "v": 4.6616,
    "w": 0.0088,
    "x": 0.0755,
    "y": 1.9093,
    "\u00fd": 1.0721,
    "z": 2.1987,
    "\u017e": 0.9952
 }

function generator(index) {
    let row = document.createElement("div")
    document.getElementById("content").appendChild(row)
    row.classList.add("border", "border-primary", "rounded-2", "row", "p-2", "m-2")

    let col1 = document.createElement("div")
    row.appendChild(col1)
    col1.classList.add("col-auto")
    col1.innerHTML = "Další slovo: "

    let col2 = document.createElement("div")
    row.appendChild(col2)
    col2.classList.add("col-auto")
    
    let code = document.createElement("code")
    col2.appendChild(code)
    code.id = index
    code.innerHTML = "Ještě nevím"

    let col3 = document.createElement("div")
    row.appendChild(col3)
    col3.classList.add("col-auto")
    col3.innerHTML = "Zadej, které slovo sis vybral: "

    let col4 = document.createElement("div")
    row.appendChild(col4)
    col4.classList.add("col")

    let inp = document.createElement("input")
    col4.appendChild(inp)
    inp.classList.add("form-control")
    inp.type = "text"
    inp.id = index + "-vybrane"

    let col5 = document.createElement("div")
    row.appendChild(col5)
    col5.classList.add("col-auto")
    col5.innerHTML = "Zadej výsledek: "

    let col6 = document.createElement("div")
    row.appendChild(col6)
    col6.classList.add("col")

    let inp2 = document.createElement("input")
    col6.appendChild(inp2)
    inp2.classList.add("form-control")
    inp2.type = "text"
    inp2.id = index + "-result"

    let col7 = document.createElement("div")
    row.appendChild(col7)
    col7.classList.add("col-auto")

    let button = document.createElement("button")
    col7.appendChild(button)
    button.classList.add("btn", "btn-outline-primary")
    button.innerHTML = "Najít další slovo"
    button.type = "button"
    button.id = index + "-button"
    button.addEventListener("click", function() {orezat_databazi(index)})
}

function orezat_databazi(index) {
    slova.push(document.getElementById(index + "-vybrane").value)
    let input = document.getElementById(index + "-result").value
    let new_db
    if (input) {
        temp_db = [...dbs[dbs.length-1]]
        for (let i=0;i<input.length;i++) {
            let inkriminovany_char = slova[slova.length-1].charAt(i)
            new_db = new Array
            if (input.charAt(i) == "0") {
                for (let j=0;j<temp_db.length;j++) {
                    let slovo = temp_db[j]
                    if (slovo.includes(inkriminovany_char)) {
                    } else {
                        new_db.push(slovo)
                    }
                }
                temp_db = [...new_db]
            } else if (input.charAt(i) == "1") {
                for (let j=0;j<temp_db.length;j++) {
                    let slovo = temp_db[j]
                    if (slovo.includes(inkriminovany_char)) {
                        new_db.push(slovo)
                    }
                }
                temp_db = [...new_db]
            } else if (input.charAt(i) == "2") {
                for (let j=0;j<temp_db.length;j++) {
                    let slovo = temp_db[j]
                    if (slovo.charAt(i) == inkriminovany_char) {
                        new_db.push(slovo)
                    }
                }
                temp_db = [...new_db]
            } else {
                console.log("unknown char: " + input.charAt(i))
            }
        }
    } else {
        alert("Musíš něco napsat.")
    }
    console.log(temp_db, Object.keys(new_db).length, "from orezavani")

    if (dbs.length-1==index) { //prepise nebo pushne novou
        dbs.push(temp_db)
    } else {
        dbs[index+1] = temp_db
    }
    temp_db = []
    odeslat_slovo(index+1)

}

function best_word(index) {
    let ohodnocena_db = []
    console.log(dbs, index, "at bestword")
    for (let i=0;i<dbs[index].length;i++) {
        let relevantni_pismenka = new Set(dbs[index][i])
        let value = 0
        relevantni_pismenka = Array.from(relevantni_pismenka)
        for (let j=0;j<relevantni_pismenka.length;j++) {
            value += cetnosti[relevantni_pismenka[j]]
        }
        ohodnocena_db.push({key: dbs[index][i], value: value})
    }

    ohodnocena_db.sort((a,b) => { //seřadí jí to
        return b.value - a.value
    })

    let result = ""
    
    for (let i = 0;i<ohodnocena_db.length;i++) {
        if (i==10) {
            break
        } else {
            result += " " + ohodnocena_db[i]["key"]
        }
    }
    return result
}

function odeslat_slovo(index) {
    let slovo = best_word(index)
    document.getElementById(index).innerHTML = slovo
}

for (let i=0;i<6;i++) {
    generator(i, db)
}

odeslat_slovo(0)

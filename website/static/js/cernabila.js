import httpGet from "./httpGet.js"

let slovo = JSON.parse(httpGet("/visuals/cerna_bila_get_word"))["slovo"]
let input = document.getElementById("input")
input.addEventListener("keypress", function() {
    if (event.key == "Enter") {
        handler(input.value)
    }
})
document.getElementById("button").addEventListener("click",function() {handler(input.value)})
document.getElementById("podat").addEventListener("click", function() {document.getElementById("reseni").innerHTML = slovo})


function zbavit_se_carek(str) {
    let carky = ["áa","ée","íi","óo","úu","ůu","ýy",]
    for (let pair of carky) {
        str = str.replace(pair[0], pair[1])
    }
    return str
}

function vyhodnot(origo_slovo, origo_navrh) {
    let slovo = zbavit_se_carek(origo_slovo)
    let navrh = zbavit_se_carek(origo_navrh)
    let vysledek = []
    let cerne_indexy = []
    let nove_slovo = ""
    let novy_navrh = ""

    // hledam cerna pismenka
    for (let i=0;i<5;i++) {
        if (slovo[i] == navrh[i]) {
            vysledek.push("černá")
            cerne_indexy.push(i)
        }
    }

    // odebiram pismenka na cernych indexech
    for (let i=0;i<5;i++) {
        if (cerne_indexy.includes(i)) {
        } else {
            nove_slovo += slovo[i]
            novy_navrh += navrh[i]
        }
    }
    // hledam bila pismenka
    for (let char of novy_navrh) {
        let nove_slovo_novy_arr = []
        let nove_slovo_arr = nove_slovo.split("")
        for (let podezrely of nove_slovo_arr) {
            if (char == podezrely) {
                vysledek.push("bílá")
                break
            } else {
                nove_slovo_novy_arr.push(podezrely)
            }
        }
        nove_slovo = nove_slovo_novy_arr.join("")
    }

    if (vysledek.length == 0) {
        return "nic"
    } else if (slovo == navrh) {
        return "Konec hry, uhodnuto! Moje slovo je: " + origo_slovo
        }
    else {
        return vysledek.join(" ")
    }
}

function handler(navrh) {
    if (navrh.length == 5) {
        document.getElementById("slovo").innerHTML = navrh
        document.getElementById("vysledek").innerHTML = vyhodnot(slovo, navrh)
        input.value = ""
    } else {
        alert("Zadej prosím slovo, které má právě 5 písmen.")
    }

}
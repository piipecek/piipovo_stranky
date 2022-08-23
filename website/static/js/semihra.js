let jmena_textarea = document.getElementById("jmena")
let indicie_textarea = document.getElementById("indicie")
let jmena_priklad_button = document.getElementById("jmena_priklad_button")
let indicie_priklad_button = document.getElementById("indicie_priklad_button")
let budiz = document.getElementById("budiz")
let karty_div = document.getElementById("karty")
let vysledek_div = document.getElementById("vysledek")
let download_button = document.getElementById("download")

let jmena_priklad = "Alice, Bob, Cyril, Dominik, Eva, Filip, Gray"
let indicie_priklad = "Tvůj dílek je v hrníčku. Hrníček je puntíkovanej. Puntíkovaná věc je ve skříni v jídelně.\nTvůj dílek je nalepený zespoda. Nalepená věc je zespoda stolu. Stůl je v zasedačce.\nTvůj dílek je za papírem. Papír je přišpendlený špendlíkem. Špendlík je na futru dveří na záchod.\nTvůj dílek je pod hrncem. Hrnec je na sporáku. Sporák je v šatně.\nTvůj dílek je v talíři. Talíř je v botníku. Botník je na střeše.\nTvůj dílek je mezi  knížkami. Knížky jsou na poličce. Polička je v společenské místnosti.\nTvůj dílek je v klobouku. Klobouk je v baťohu. Baťoh je u dveří ven."
let res

jmena_priklad_button.addEventListener("click", function() {
    if (jmena_textarea.value == "") {
        jmena_textarea.value = jmena_priklad
    } else {
        alert("Abych mohl předvyplnit příklad pro jména, musí být to pole prázdné.")
    }
})

indicie_priklad_button.addEventListener("click", function() {
    if (indicie_textarea.value == "") {
        indicie_textarea.value = indicie_priklad
    } else {
        alert("Abych mohl předvyplnit příklad pro indicie, musí být to pole prázdné.")
    }
})

budiz.addEventListener("click", function() {
    if (jmena_textarea.value == "") {
        alert("Jména jsou prázdná. Něco tam napiš.")
    }
    else if (indicie_textarea.value == "") {
        alert("Indicie jsou prázdné. Něco tam napiš.")
    } else {
        $.ajax({
            data : {
                jmena: jmena_textarea.value,
                indicie: indicie_textarea.value
            },
            type: "POST",
            url: "/visuals/semihra"
        })
        .done(function(data) {
            vysledek_handle(data)
            res = JSON.parse(data)
        })
    }
})

download_button.addEventListener("click", function() {
    let a = document.createElement("a")
    let file = new Blob([JSON.stringify(res, null, 4)], {type: "text/plain"})
    a.href = URL.createObjectURL(file)
    a.download = "semihra.json"
    a.click()
})

function vysledek_handle(data) {
    data = JSON.parse(data)
    vysledek_div.hidden = false
    karty_div.replaceChildren()
    if (data.length == 1) {
        alert(data[0])
    } else {
        for (karta of data) {
            karty_div.appendChild(generator_karty(karta["jmeno"], karta["mluvis_s"], karta["uvodni_veta"], karta["dale_vis"]))
        }
    }
}

function generator_karty(jmeno, mluvis_s, uvodni_veta, dale_vis) {
    let div = document.createElement("div")
    div.classList.add("border", "border-primary", "rounded-2", "p-2", "m-2")

    let jmeno_nadpis = document.createElement("h3")
    jmeno_nadpis.innerHTML = "Jméno: "
    let jmeno_content = document.createElement("p")
    jmeno_content.innerHTML = jmeno

    let mluvis_s_nadpis = document.createElement("h3")
    mluvis_s_nadpis.innerHTML = "Můžeš mluvit s: "
    let mluvis_s_list = document.createElement("ul")
    for (let clovek of mluvis_s) {
        let li = document.createElement("li")
        li.innerHTML = clovek
        mluvis_s_list.appendChild(li)
    }

    let zacatek_nadpis = document.createElement("h3")
    zacatek_nadpis.innerHTML = "Tvůj začátek: "
    let zacatek_content = document.createElement("p")
    zacatek_content.innerHTML = uvodni_veta

    let dale_vis_nadpis = document.createElement("h3")
    dale_vis_nadpis.innerHTML = "Dále víš, že: "
    let dale_vis_list = document.createElement("ul")
    for (let vis of dale_vis) {
        let li = document.createElement("li")
        li.innerHTML = vis
        dale_vis_list.appendChild(li)
    }

    div.appendChild(jmeno_nadpis)
    div.appendChild(jmeno_content)
    div.appendChild(mluvis_s_nadpis)
    div.appendChild(mluvis_s_list)
    div.appendChild(zacatek_nadpis)
    div.appendChild(zacatek_content)
    div.appendChild(dale_vis_nadpis)
    div.appendChild(dale_vis_list)

    return div
}   


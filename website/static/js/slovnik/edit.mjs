let slovicko_element = document.getElementById("slovicko")
let jazyky = JSON.parse(document.getElementById("jazyky").value)
let jazyky_inputs = document.getElementById("jazyky_inputs")
let druh_element = document.getElementById("druh")
let asociace_element = document.getElementById("asociace")
let kategorie_element = document.getElementById("kategorie")
let slovicko;

document.getElementById("potvrdit").onclick = update_slovicko


function update_slovicko() {
    for (let i=0; i<jazyky.length;i++) {
        if (document.getElementById(jazyky[i]).value == "") {
            slovicko["v_jazyce"][jazyky[i]] = []
        } else {
            slovicko["v_jazyce"][jazyky[i]] = document.getElementById(jazyky[i]).value.split(", ")
        }
    }

    if (druh_element.value == "") {
        slovicko["druh"] = []
    } else {
        slovicko["druh"] = druh_element.value.split(", ")
    }
    if (kategorie_element.value == "") {
        slovicko["kategorie"] = []
    } else {
        slovicko["kategorie"] = kategorie_element.value.split(", ")
    }
    if (asociace_element.value == "") {
        slovicko["asociace"] = []
    } else {
        slovicko["asociace"] = asociace_element.value.split(", ")
    }
    slovicko_element.value = JSON.stringify(slovicko)
}

function on_load() {
    slovicko = JSON.parse(slovicko_element.value)
    for (let i=0; i<jazyky.length;i++) {
        let inp = document.createElement("input")
        let lab = document.createElement("label")
        inp.id = jazyky[i]
        lab.for = jazyky[i]
        lab.innerHTML = jazyky[i] + ":"
        inp.type = "text"
        inp.value = slovicko["v_jazyce"][jazyky[i]].join(", ")
        jazyky_inputs.appendChild(lab)
        jazyky_inputs.appendChild(inp)
        jazyky_inputs.appendChild(document.createElement("br"))
    }
    druh_element.value = slovicko["druh"].join(", ")
    kategorie_element.value = slovicko["kategorie"].join(", ")
    asociace_element.value = slovicko["asociace"].join(", ")
}

on_load()
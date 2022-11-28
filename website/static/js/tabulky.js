let stahnout_button = document.getElementById("stahnout")
let nacist_tabulku = document.getElementById("nacist")
let input = document.getElementById("nahrat")
let tabulka_div = document.getElementById("tabulka")
let nova = document.getElementById("nova")
let vygenerovat = document.getElementById("vygenerovat")
let latexfield = document.getElementById("latex")

stahnout_button.addEventListener("click", function() {odeslat(generovat_json())})
nacist_tabulku.addEventListener("click", nacist)
nova.addEventListener("click", function() {novej_radek("","")})
vygenerovat.addEventListener("click", generovat)

function generovat_json() {
    let data = {}
    for (let radek of tabulka_div.children) {
        let name = radek.childNodes[0].childNodes[0].value
        let cisla = radek.childNodes[1].childNodes[0].value.split(",")
        let cisla_parsed = []
        for (let c of cisla) {
            cisla_parsed.push(parseFloat(c))
        }
        data[name] = cisla_parsed
    }
    return data
}

function odeslat(data) {

    if (Object.entries(data).length == 0) {
        alert("Nemáš žádnou tabuoku ke stažení")
    } else {
        let a = document.createElement("a")
        let file = new Blob([JSON.stringify(data, null, 4)], {type: "text/plain"})
        a.href = URL.createObjectURL(file)
        a.download = "data.json"
        a.click()
    }
}

function nacist() {
    let child = tabulka_div.firstElementChild
    while (child) {
        tabulka_div.removeChild(child)
        child = tabulka_div.lastElementChild
    }
    let file = input.files[0]
    if (file) {
        let fr = new FileReader()
        fr.readAsText(file)
        fr.onload = function() {
            let parsed = JSON.parse(fr.result)
            for (let entry of Object.entries(parsed)) {
                novej_radek(entry[0], entry[1])
            }
        }
    } else {
        alert("Nenahrál jsi žádnej soubor")
    }
}

function novej_radek(name, data) {
    let div = document.createElement("div")
    div.classList.add("row", "my-1")
    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    div.appendChild(col1)
    let col2 = document.createElement("div")
    col2.classList.add("col")
    div.appendChild(col2)
    let name_input = document.createElement("input")
    name_input.classList.add("form-control")
    name_input.value = name
    col1.appendChild(name_input)
    let data_input = document.createElement("input")
    data_input.classList.add("form-control")
    data_input.value = data
    col2.appendChild(data_input)
    tabulka_div.appendChild(div)
}

function generovat() {
    let data = Object.entries(generovat_json())
    let result = "\\begin{table}[h] \n \t \\centering \n \t \\begin{tabular}{"
    let cecka = "|c||" // ano, udela to dohromady první ||
    for (let i of data[0][1]) {
        cecka += "c|"
    }
    result += cecka
    result += "} \n \t \t \\hline \n"
    // tady
    let radky = []
    for (let entry of data) {
        let radek = "\t \t "
        radek += entry[0]
        radek += " & "
        radek += entry[1].join(" & ")
        radek += " \\\\"
        radky.push(radek)
    }

    result += radky.join(" \n \t \t \\hline \n")

    result += "\n \t \t \\hline \n\t \\end{tabular}\n\t \\caption{Caption}\n\t \\label{tab:my_label}\n \\end{table}"
    latexfield.value = result

    let pocet_radku_tabulky = data.length
    latexfield.rows = pocet_radku_tabulky*2 + 8

}
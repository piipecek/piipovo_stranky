import httpGet from "./httpGet.js"

let chyby = JSON.parse(httpGet("/send_noauth/chyby"))
let content_div = document.getElementById("content")
let save_button = document.getElementById("save_button")
let result = document.getElementById("result")


save_button.addEventListener("click", vyhodnotit)

function vyhodnotit() {
    chyby = []
    for (let i = 0; i<content_div.children.length;i++) {
        let zaznam = {}
        zaznam["autor"] = content_div.children[i].children[0].children[1].innerHTML
        zaznam["popis"] = content_div.children[i].children[1].children[1].innerHTML
        zaznam["stav"] =  content_div.children[i].children[2].children[1].children[0].value
        chyby.push(zaznam)
    }
    result.value = JSON.stringify(chyby)
    document.getElementById("form").submit()
}

function smazat_zaznam(div_id) {
    document.getElementById(div_id).remove()
}

function generator(index, data) { 
    let div = document.createElement("div")
    content_div.appendChild(div)
    div.classList.add("border", "rounded-2", "border-secondary", "my-2", "p-2")
    div.id = String(index) + "na_delete"


    function row_generator() {

        let row = document.createElement("div")
        row.classList.add("row", "my-1")
        div.appendChild(row)

        let col1 = document.createElement("div")
        row.appendChild(col1)
        col1.classList.add("col-3")
    
        let col2 =document.createElement("div")
        row.appendChild(col2)
        col2.classList.add("col")

        return [col1, col2]

    }

    let cols_array = row_generator()
    cols_array[0].innerHTML = "Autor"
    cols_array[1].innerHTML = data["autor"]

    cols_array = row_generator()
    cols_array[0].innerHTML = "Popis:"
    cols_array[1].innerHTML = data["popis"]

    cols_array = row_generator()
    cols_array[0].innerHTML = "Stav řešení:"
    let field = document.createElement("input")
    cols_array[1].appendChild(field)
    field.value = data["stav"]
    field.classList.add("form-control")


    let smazat_button = document.createElement("button")
    div.appendChild(smazat_button)
    smazat_button.innerHTML = "Smazat záznam o chybě"
    smazat_button.type = "button"
    smazat_button.classList.add("btn", "btn-outline-danger")
    smazat_button.addEventListener("click", function()  {smazat_zaznam(div.id)})

}

for (let i=0;i<chyby.length;i++) {
    generator(i, chyby[i])
}

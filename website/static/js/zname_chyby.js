import httpGet from "./httpGet.js"

let chyby = JSON.parse(httpGet("/send_noauth/chyby"))
let content_div = document.getElementById("content")

function generator(data) {
    let div = document.createElement("div")
    content_div.appendChild(div)
    div.classList.add("border", "rounded-2", "border-secondary", "my-2", "p-2")
    div.classList.add("bug")

    function row_generator() {

        let row = document.createElement("div")
        row.classList.add("row", "my-1")
        div.appendChild(row)

        let col1 = document.createElement("div")
        row.appendChild(col1)
        col1.classList.add("col-2")
    
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
    cols_array[1].innerHTML = data["stav"]
}

for (let i=0;i<chyby.length;i++) {
    generator(chyby[i])
}

import httpGet from "./httpGet.js"

let users_from_data_folder = JSON.parse(httpGet("/send_admin/users_from_data_folder"))
let users_from_db = JSON.parse(httpGet("/send_admin/users_from_db"))

function generator_from_folder(id, pocet_slovicek, jazyky) {
    let row = document.createElement("div")
    row.classList.add("row", "my-2")
    document.getElementById("from_data_folder").appendChild(row)

    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    row.appendChild(col1)
    col1.innerHTML = id

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)
    col2.innerHTML = jazyky

    let col3 = document.createElement("div")
    col3.classList.add("col-auto")
    row.appendChild(col3)
    col3.innerHTML = pocet_slovicek

    let button = document.createElement("button")
    button.classList.add("btn", "btn-danger")
    button.type = "button"
    button.innerHTML = "smazat usera"
    button.addEventListener("click", function() {smazat_usera(id)})

    let col4 = document.createElement("div")
    col4.classList.add("col-auto")
    row.appendChild(col4)
    col4.appendChild(button)
    
}

function smazat_usera(id) {
    document.getElementById("result").value = id
    document.getElementById("form").submit()
}

for (let i=0;i<users_from_data_folder.length;i++) {
    generator_from_folder(users_from_data_folder[i]["id"], users_from_data_folder[i]["pocet_slovicek"], String(users_from_data_folder[i]["settings"]["jazyky"]))
}

function generator_from_db(id, email) {
    let row = document.createElement("div")
    row.classList.add("row", "my-2")
    document.getElementById("from_db").appendChild(row)

    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    row.appendChild(col1)
    col1.innerHTML = id

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)
    col2.innerHTML = email
}

for (let i=0;i<users_from_db.length;i++) {
    generator_from_db(users_from_db[i]["id"], String(users_from_db[i]["email"]))
}

document.getElementById("db_count").innerHTML = users_from_db.length
document.getElementById("folder_count").innerHTML = users_from_data_folder.length


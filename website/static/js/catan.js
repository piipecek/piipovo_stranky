let buttons = document.getElementsByClassName("cudlitka")
let generate_button = document.getElementById("generate")

for (let i=0;i<buttons.length;i++) {
    buttons[i].addEventListener("click", function() {button_pressed(buttons[i].id)})
}
generate_button.addEventListener("click", send)

let result = {
    "force_desert": false,
    "adjacent_land": false,
    "ports": false,
    "adjacent_values": false,
    "unique_68": true,
    "adjacent_68": false
}

function button_pressed(id_name) {
    if (id_name.includes("_yes")) {
        id_name_druheho = id_name.replace("_yes", "_no")
        name_do_resultu = id_name.replace("_yes", "")
        result[name_do_resultu] = true
    } else {
        id_name_druheho = id_name.replace("_no", "_yes")
        name_do_resultu = id_name.replace("_no", "")
        result[name_do_resultu] = false
    }
    document.getElementById(id_name).classList.add("btn-success")
    document.getElementById(id_name).classList.remove("btn-outline-success")
    document.getElementById(id_name_druheho).classList.add("btn-outline-success")
    document.getElementById(id_name_druheho).classList.remove("btn-success")
}

function send() {
    console.log(result)
}
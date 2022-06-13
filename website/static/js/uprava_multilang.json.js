pridat_button = document.getElementById("pridat")
generate_button = document.getElementById("generate")

pridat_button.addEventListener("click", function() {
    document.getElementById("content").appendChild(nove_pole("","","",""))
})

generate_button.addEventListener("click", generate_json)


document.getElementById("formFile").addEventListener('change', function() {
        var fr=new FileReader();
        fr.addEventListener("load",function(){
            res = fr.result;
            generate(res)
        })
        fr.readAsText(this.files[0]);
        })

function nove_pole(name, location, cs, en) {
    let pole = document.createElement("div")
    pole.classList.add("p-2", "m-2", "border", "border-primary", "rounded-2")
    
    let row = document.createElement("div")
    row.classList.add("row", "my-1")
    pole.appendChild(row)
    
    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    col1.innerHTML = "Name: "
    row.appendChild(col1)

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)
    
    let name_input = document.createElement("input")
    name_input.type="text"
    name_input.classList.add("form-control")
    name_input.value = name
    col2.appendChild(name_input)

    let col3 = document.createElement("div")
    col3.classList.add("col-auto")
    col3.innerHTML = "Location: "
    row.appendChild(col3)

    let col4 = document.createElement("div")
    col4.classList.add("col")
    row.appendChild(col4)

    let location_input = document.createElement("input")
    location_input.type="text"
    location_input.classList.add("form-control")
    location_input.value = location
    col4.appendChild(location_input)


    
    let row2 = document.createElement("div")
    row2.classList.add("row", "my-1")
    pole.appendChild(row2)

    let col1row2 = document.createElement("div")
    col1row2.classList.add("col-auto")
    col1row2.innerHTML = "cs:"
    row2.appendChild(col1row2)

    let col2row2 = document.createElement("div")
    col2row2.classList.add("col")
    row2.appendChild(col2row2)

    let cs_input = document.createElement("input")
    cs_input.type = "text"
    cs_input.classList.add("form-control")
    cs_input.value = cs
    col2row2.appendChild(cs_input)




    let row3 = document.createElement("div")
    row3.classList.add("row", "my-1")
    pole.appendChild(row3)

    let col1row3 = document.createElement("div")
    col1row3.classList.add("col-auto")
    col1row3.innerHTML = "en:"
    row3.appendChild(col1row3)

    let col2row3 = document.createElement("div")
    col2row3.classList.add("col")
    row3.appendChild(col2row3)

    let en_input = document.createElement("input")
    en_input.type="text"
    en_input.classList.add("form-control")
    en_input.value = en
    col2row3.appendChild(en_input)


    return pole
}

function generate(raw_text) {
    let data = JSON.parse(raw_text)
    soubor_je_vporadku = true
    problematicky_zaznam = ""
    //check formatu
    for (zaznam of data) {
        if ("name" in zaznam && "location" in zaznam  && "cs" in zaznam["translations"] && "en" in zaznam["translations"]) {
        } else {
            soubor_je_vporadku = false
            problematicky_zaznam = JSON.stringify(zaznam)
        }
    }
    if (soubor_je_vporadku) {
        pridat_button.hidden = false
        generate_button.hidden = false
        document.getElementById("content").innerHTML = "" // clearne cokoli predchoziho
        for (zaznam of data) {
            document.getElementById("content").appendChild(nove_pole(zaznam["name"], zaznam["location"], zaznam["translations"]["cs"],zaznam["translations"]["en"]))
        }
    } else {
        alert("Soubor neměl správný formát, problematický záznam je " + problematicky_zaznam)
    }
}

function generate_json() {
    let res = []
    for (let pole of document.getElementById("content").childNodes) {
        let name = pole.childNodes[0].childNodes[1].childNodes[0].value
        let location = pole.childNodes[0].childNodes[3].childNodes[0].value
        let cs = pole.childNodes[1].childNodes[1].childNodes[0].value
        let en = pole.childNodes[2].childNodes[1].childNodes[0].value

        res.push({
            "name": name,
            "location": location,
            "translations": {
                "cs": cs,
                "en": en
            }
        })
    }
    

    // stažení json objektu
    let a = document.createElement("a")
    let file = new Blob([JSON.stringify(res, null, 4)], {type: "text/plain"})
    a.href = URL.createObjectURL(file)
    a.download = "multilang.json"
    a.click()
}
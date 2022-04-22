console.log("here")

let in_field = document.getElementById("in")
let out_field = document.getElementById("out")
in_field.addEventListener("input", update)


function update() {
    console.log(in_field.value)
    out_field.value = convert(in_field.value)
}

function convert(text) {
    let chars = {
        "á":"\\'{a}",
        "é":"\\'{e}",
        "ě":"\\v{e}",
        "í":"\\'{i}",
        "ó":"\\'{o}",
        "ú":"\\'{u}",
        "ů":"\\r{u}",
        "ý":"\\'{y}",
        "ž":"\\v{z}",
        "š":"\\v{s}",
        "č":"\\v{c}",
        "ř":"\\v{r}",
        "ď":"\\hbox{d\\kern-1.5pt'}",
        "ť":"\\hbox{t\\kern-1.5pt'}",
        "ň":"\\v{n}"
    }
    let result = ""
    for (let i=0;i<text.length;i++){
        console.log("here", text[i], text[i] in chars)
        if (text[i] in chars) {
            result += chars[text[i]]
        } else {
            result += text[i]
        }
    }
    return result
}

update()
let jazyky = JSON.parse(document.getElementById("jazyky").value)
let jazyky_div = document.getElementById("jazyky_dropdowns")
let btn = document.getElementById("new_jazyk_dropdown")

btn.onclick = novy_jazyk_dropdown

function novy_jazyk_dropdown() {
    if ((jazyky_div.childElementCount + 1 )/2 < jazyky.length) {
        let s = document.createElement("select")
        s.name = "dropdown_jazyka"
        let opt1 = document.createElement("option")
        opt1.value=""
        opt1.innerHTML = "- Vyberte jazyk -"
        s.appendChild(opt1)
        for (let i=0;i<jazyky.length;i++) {
            let opt = document.createElement("option")
            opt.value = jazyky[i]
            opt.innerHTML = jazyky[i]
            s.appendChild(opt.cloneNode(true))
        }
        if (jazyky_div.childElementCount == 0) {
            jazyky_div.appendChild(s)
        } else {
            let span = document.createElement("span")
            span.innerHTML = " - "
            jazyky_div.appendChild(span)
            jazyky_div.appendChild(s)
        }
    } else {
        alert("Už nemá smysl přidávat další jazyk, tvůj slovník umí jen tolik různých jazyků.")
    }
    
}

novy_jazyk_dropdown()
novy_jazyk_dropdown()

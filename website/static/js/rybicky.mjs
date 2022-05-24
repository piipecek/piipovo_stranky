// imports
import {move} from "./rybicky_move.mjs"

// other declarations
let debug_create = false
let ryby = [];
let req;
let ukazat_polomer_dohledu_bool = false;
let ukazat_sirku_zony_bool = false;
let ukazat_osobni_polomer_bool = false;
let ukazat_prostor_usmernovani_bool = false; 
let start_je_kruh = false;
let color = "blue";
let v;
let velikost_ryby;
let koef_pritahovaci;
let polomer_dohledu;
let sirka_zony;
let koef_od_kraju;
let koef_odpuzovaci;
let osobni_polomer;
let koef_usmernovaci;
let prostor_usmernovani;
let n;


// constants
const velikost_ryby_element = document.getElementById("velikost_ryby");
const rychlost_element = document.getElementById("rychlost");
const koef_pritahovani_element = document.getElementById("koef_pritahovani")
const polomer_dohledu_element =document.getElementById("polomer_dohledu");
const pocet_ryb_element = document.getElementById("pocet_ryb");
const sirka_zony_element = document.getElementById("sirka_zony");
const koef_od_kraju_element = document.getElementById("koef_od_kraju");
const polomer_dohledu_button = document.getElementById("polomer_dohledu_button");
const sirka_zony_button = document.getElementById("sirka_zony_button");
const koef_odpuzovaci_element = document.getElementById("koef_odpuzovaci");
const osobni_prostor_element = document.getElementById("osobni_prostor");
const osobni_prostor_button = document.getElementById("osobni_prostor_button");
const koef_usmernovaci_element = document.getElementById("koef_usmernovaci");
const prostor_usmernovani_element = document.getElementById("prostor_usmernovani");
const prostor_usmernovani_button = document.getElementById("prostor_usmernovani_button");
const startovni_pozice_button = document.getElementById("typ_startu");
const restart_button = document.getElementById("restart")
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
// const width = 0.9 * window.innerWidth;
// const height = 0.9 * window.innerHeight;

// Konstantní šířka canvasu zaručí, že rybičky budou mít pořád stejně
// velký prostor na plavání i na malých/úzkých obrazovkách.
const window_aspect_ratio = window.innerWidth / window.innerHeight;
const aspect_threshold = 0.6;
const width_threshold = 880;
const is_small_device = (window_aspect_ratio < aspect_threshold || window.innerWidth < width_threshold);
const aspect_ratio = is_small_device ? 1 : 0.5; // Mobily/tablety mají čtvercový canvas
const width = is_small_device ? 500 : 1000; // Menší render width pro mobily/tablety
const height = aspect_ratio * width;
canvas.width = width;
canvas.height = height;
canvas.style.setProperty("--aspect-ratio", aspect_ratio);

//event listeners
velikost_ryby_element.oninput = changed_velikost_ryby
rychlost_element.oninput = changed_rychlost
koef_pritahovani_element.oninput = changed_koef_pritahovani
polomer_dohledu_element.oninput = changed_polomer_dohledu
pocet_ryb_element.onchange = changed_pocet_ryb
sirka_zony_element.oninput = changed_sirka_zony
koef_od_kraju_element.oninput = changed_koef_od_kraju
sirka_zony_button.onclick = ukazat_sirku_zony
polomer_dohledu_button.onclick = ukazat_polomer_dohledu
koef_odpuzovaci_element.oninput = changed_koef_odpuzovaci
osobni_prostor_element.oninput = changed_osobni_prostor
osobni_prostor_button.onclick = ukazat_osobni_polomer
koef_usmernovaci_element.oninput = changed_koef_usmernovaci
prostor_usmernovani_element.oninput = changed_prostor_usmernovani
prostor_usmernovani_button.onclick = ukazat_prostor_usmernovani
startovni_pozice_button.onclick = zmenit_startovni_pozici
restart_button.onclick = changed_pocet_ryb


// event handlers
function changed_velikost_ryby() {
    velikost_ryby = parseInt(velikost_ryby_element.value)/2;
    document.getElementById("velikost_ryby_display").innerHTML = velikost_ryby_element.value
    changed_polomer_dohledu()
    changed_prostor_usmernovani()
    changed_osobni_prostor()
}
function changed_rychlost() {
    v = parseInt(rychlost_element.value)/100;
    document.getElementById("rychlost_display").innerHTML = rychlost_element.value
}
function changed_koef_pritahovani() {
    koef_pritahovaci = parseInt(koef_pritahovani_element.value)/5000
    document.getElementById("koef_pritahovani_display").innerHTML = koef_pritahovani_element.value
}
function changed_polomer_dohledu() {
    polomer_dohledu = (parseInt(polomer_dohledu_element.value)*velikost_ryby)/4
    document.getElementById("polomer_dohledu_display").innerHTML = polomer_dohledu_element.value
}
function changed_sirka_zony() {
    sirka_zony = parseInt(sirka_zony_element.value)
    document.getElementById("sirka_zony_display").innerHTML = sirka_zony_element.value
}
function changed_koef_od_kraju() {
    koef_od_kraju = parseInt(koef_od_kraju_element.value)/1000
    document.getElementById("koef_od_kraju_display").innerHTML = koef_od_kraju_element.value
}
function changed_koef_odpuzovaci() {
    koef_odpuzovaci = parseInt(koef_odpuzovaci_element.value)/20
    document.getElementById("koef_odpuzovaci_display").innerHTML = koef_odpuzovaci_element.value
}
function changed_osobni_prostor() {
    osobni_polomer = (parseInt(osobni_prostor_element.value)*velikost_ryby)/4
    document.getElementById("osobni_prostor_display").innerHTML = osobni_prostor_element.value
}
function changed_koef_usmernovaci() {
    koef_usmernovaci = parseInt(koef_usmernovaci_element.value)/5000
    document.getElementById("koef_usmernovaci_display").innerHTML = koef_usmernovaci_element.value
}
function changed_prostor_usmernovani() {
    prostor_usmernovani = (parseInt(prostor_usmernovani_element.value)*velikost_ryby)/4
    document.getElementById("prostor_usmernovani_display").innerHTML = prostor_usmernovani_element.value
}
function zmenit_startovni_pozici() {
    if (start_je_kruh) {
        start_je_kruh = false
        startovni_pozice_button.innerHTML = "Začínat náhodně"
    } else {
        start_je_kruh = true
        startovni_pozice_button.innerHTML = "Začínat z kruhu"
    }
}
function ukazat_polomer_dohledu() {
    if (ukazat_polomer_dohledu_bool) {
        ukazat_polomer_dohledu_bool = false
        polomer_dohledu_button.innerHTML = "Ukázat poloměr dohledu"
    } else {
        ukazat_polomer_dohledu_bool = true
        polomer_dohledu_button.innerHTML = "Skrýt poloměr dohledu"
    }
    polomer_dohledu_button.classList.toggle("active")
}
function ukazat_sirku_zony() {
    if (ukazat_sirku_zony_bool) {
        sirka_zony_button.innerHTML = "Ukázat zónu"
        ukazat_sirku_zony_bool = false
    } else {
        ukazat_sirku_zony_bool = true
        sirka_zony_button.innerHTML = "Skrýt zónu"
    }
    sirka_zony_button.classList.toggle("active")
}
function ukazat_osobni_polomer() {
    if (ukazat_osobni_polomer_bool) {
        osobni_prostor_button.innerHTML = "Ukázat prostor ryby"
        ukazat_osobni_polomer_bool = false
    } else {
        osobni_prostor_button.innerHTML = "Skrýt prostor ryby"
        ukazat_osobni_polomer_bool = true
    }
    osobni_prostor_button.classList.toggle("active")
}
function ukazat_prostor_usmernovani() {
    if (ukazat_prostor_usmernovani_bool) {
        prostor_usmernovani_button.innerHTML = "Ukázat prostor usměrňování"
        ukazat_prostor_usmernovani_bool = false
    } else {
        prostor_usmernovani_button.innerHTML = "Skrýt prostor usměrňování"
        ukazat_prostor_usmernovani_bool = true
    }
    prostor_usmernovani_button.classList.toggle("active")
}
function changed_pocet_ryb() {
    n = parseInt(pocet_ryb_element.value);
    if (req) {
        cancelAnimationFrame(req);
    }
    ctx.clearRect(0,0,width,height);
    ryby = [];
    create_ryby();
    update();
}


// class Ryba
class Ryba {
    constructor(x, y, dx, dy, id) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.dx = dx
        this.dy = dy
        this.novex = x;
        this.novey = y;
        this.novedx = dx;
        this.novedy =dy;
    }
    draw() {
        let velikost_dx_dy = Math.sqrt(this.dx**2 + this.dy**2)
        let smerovy_vektor = [this.dx/velikost_dx_dy, this.dy/velikost_dx_dy]
        let alpha = Math.acos(smerovy_vektor[0])
        if (smerovy_vektor[1] < 0) { // jsem za pi
            alpha = Math.PI*2-alpha
        }
        let beta = alpha + (4*Math.PI)/3
        let gamma = alpha + (2*Math.PI)/3
        let A = [this.x + velikost_ryby*Math.cos(alpha), this.y + velikost_ryby*Math.sin(alpha)]
        let B = [this.x + velikost_ryby*Math.cos(beta), this.y + velikost_ryby*Math.sin(beta)]
        let C = [this.x + velikost_ryby*Math.cos(gamma), this.y + velikost_ryby*Math.sin(gamma)]
        
        ctx.fillStyle = color
        ctx.beginPath();
        ctx.moveTo(this.x, this.y)
        ctx.lineTo(C[0], C[1])
        ctx.lineTo(A[0], A[1])
        ctx.lineTo(B[0], B[1])
        ctx.lineTo(this.x, this.y)
        ctx.fill()

        if (ukazat_osobni_polomer_bool) {
            ctx.strokeStyle = "orange"
            ctx.lineWidth = 1
            ctx.beginPath()
            ctx.arc(this.x,this.y,osobni_polomer,0,Math.PI*2)
            ctx.stroke()
        }

        if (ukazat_polomer_dohledu_bool) {
            ctx.strokeStyle = "lightgreen"
            ctx.lineWidth = 1
            ctx.beginPath()
            ctx.arc(this.x,this.y,polomer_dohledu,0,Math.PI*2)
            ctx.stroke()
        }
        if (ukazat_prostor_usmernovani_bool) {
            ctx.strokeStyle = "red"
            ctx.lineWidth = 1
            ctx.beginPath()
            ctx.arc(this.x,this.y,prostor_usmernovani,0,Math.PI*2)
            ctx.stroke()
        }

    }
}


//funkce co akualy neco delaj
function update() {
    ctx.clearRect(0,0,width, height);

    if (ukazat_polomer_dohledu_bool) {
        ctx.strokeStyle = "lightgreen"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(width/2,height/2,polomer_dohledu,0,Math.PI*2)
        ctx.stroke()
    }
    if (ukazat_prostor_usmernovani_bool) {
        ctx.strokeStyle = "red"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(width/2,height/2,prostor_usmernovani,0,Math.PI*2)
        ctx.stroke()
    }
    if (ukazat_osobni_polomer_bool) {
        ctx.strokeStyle = "orange"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(width/2,height/2,osobni_polomer,0,Math.PI*2)
        ctx.stroke()
    }
    if (ukazat_sirku_zony_bool) {
        ctx.strokeStyle = "lightblue"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.moveTo(sirka_zony, sirka_zony)
        ctx.lineTo(width-sirka_zony, sirka_zony)
        ctx.lineTo(width-sirka_zony, height-sirka_zony)
        ctx.lineTo(sirka_zony, height-sirka_zony)
        ctx.lineTo(sirka_zony,sirka_zony)
        ctx.stroke()
    }
    let data = {
        "ryby": ryby,
        "v": v,
        "width": width,
        "height": height,
        "sirka_zony": sirka_zony,
        "koef_od_kraju": koef_od_kraju,
        "koef_odpuzovaci":koef_odpuzovaci,
        "koef_pritahovaci": koef_pritahovaci,
        "polomer_dohledu": polomer_dohledu,
        "osobni_polomer": osobni_polomer,
        "koef_usmernovaci": koef_usmernovaci,
        "prostor_usmernovani": prostor_usmernovani
    }
    ryby = move(data)
    for (let i=0;i<n;i++) {
        ryby[i].draw()
    }
    req = requestAnimationFrame(update)
}

function create_ryby() {
    if (!debug_create) {
        if (start_je_kruh) {
            let R = Math.min(width-2*sirka_zony, height-2*sirka_zony)*0.9/2
            let dphi = Math.PI*2/n
            for (let i=0; i<n; i++) {
                let x = width/2 + R*Math.cos(dphi*i)
                let y = height/2 + R*Math.sin(dphi*i)
                let dx = -Math.cos(dphi*i)
                let dy = -Math.sin(dphi*i)
                let temp = dx
                dx = dy
                dy = -temp
                let ryba = new Ryba(x,y,dx,dy,i)
                ryby.push(ryba)
            }
        } else {
            for (let i=0; i<n; i++) {
                let x = Math.random()*width
                let y = Math.random()*height
                let phi = Math.random()*Math.PI*2
                let dx = Math.cos(phi) // už produkuje jednotkovy vektor
                let dy = Math.sin(phi)
                let ryba = new Ryba(x,y,dx,dy,i)
                ryby.push(ryba)
            }
        }
    } else {
        let r1 = new Ryba(200, 200, 1, 1, 1)
        let r2 = new Ryba(600, 300, -1, -1, 2)
        ryby = [r1,r2]
    }

}


// MAIN
changed_rychlost();
changed_velikost_ryby();
changed_koef_pritahovani();
changed_polomer_dohledu();
changed_sirka_zony()
changed_koef_od_kraju()
changed_koef_odpuzovaci()
changed_osobni_prostor()
changed_koef_usmernovaci()
changed_prostor_usmernovani()
changed_pocet_ryb() // responsible za generovani prvnich ryb a zavolani update

import {Cartesian_graph} from "./cartesian_graph.js"

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
    let id_name_druheho
    let name_do_resultu
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
    document.getElementById("preloader").hidden = false
    $.ajax({
        data : {
            result: JSON.stringify(result)
        },
        type: "POST",
        url: "/visuals/catan"
    })
    .done(function(data) {
        document.getElementById("preloader").hidden = true
        draw_map(data)
    })
}

function draw_map(data) {
    data = JSON.parse(data)
    console.log(data)
    let c = new Cartesian_graph("map",1000,800,[500.5,400.5],70, true)
    document.getElementById("can").hidden = false
    let s = 0.866
    let A = [0,1]
    let B = [s, 0.5]
    let C = [s, -0.5]
    let D = [0, -1]
    let E = [-s, -0.5]
    let F = [-s, 0.5]

    let G = [0,2]
    let H = [s, 2.5]
    let I = [2*s, 2]
    let J = [2*s,1]
    let K = [3*s,0.5]
    let L = [3*s, -0.5]
    let M = [2*s,-1]
    let N = [2*s,-2]
    let O = [s, -2.5]
    let P = [0,-2]
    let Q = [-s, -2.5]
    let R = [-2*s, -2]
    let S = [-2*s,-1]
    let T = [-3*s,-0.5]
    let U = [-3*s, 0.5]
    let V = [-2*s,1]
    let W = [-2*s,2]
    let X = [-s, 2.5]

    let AA = [0,4]
    let AB = [s, 3.5]
    let AC = [2*s, 4]
    let AD = [3*s, 3.5]
    let AE = [3*s, 2.5]
    let AF = [4*s, 2]
    let AG = [4*s, 1]
    let AH = [5*s, 0.5]

    let AI = [5*s, -0.5]
    let AJ = [4*s, -1]
    let AK = [4*s, -2]
    let AL = [3*s, -2.5]
    let AM = [3*s, -3.5]
    let AN = [2*s, -4]
    let AO = [s, -3.5]
    let AP = [0,-4]

    let BD = [-s, 3.5]
    let BC = [-2*s, 4]
    let BB = [-3*s, 3.5]
    let BA = [-3*s, 2.5]
    let AZ = [-4*s, 2]
    let AY = [-4*s, 1]
    let AX = [-5*s, 0.5]

    let AW = [-5*s, -0.5]
    let AV = [-4*s, -1]
    let AU = [-4*s, -2]
    let AT = [-3*s, -2.5]
    let AS = [-3*s, -3.5]
    let AR = [-2*s, -4]
    let AQ = [-s, -3.5]

    let OA = [4*s-s/1.5,5]
    let OB = [6*s, 1]
    let OC = [6*s+s/1.5, 0]
    let OD = [4*s,-4]
    let OE = [4*s-s/1.5,-5]
    let OF = [-2*s,-5]
    let OG = [-(4*s-s/1.5),-5]
    let OH = [-6*s,-1]
    let OI = [-(6*s+s/1.5),0]
    let OJ = [-4*s,4]
    let OK = [-(4*s-s/1.5),5]
    let OL = [2*s,5]




    let small_ring = [A,B,C,D,E,F]
    let middle_ring =[G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X]
    let outer_ring = [AA,AB,AC,AD,AE,AF,AG,AH,AI,AJ,AK,AL,AM,AN,AO,AP,AQ,AR,AS,AT,AU,AV,AW,AX,AY,AZ,BA,BB,BC,BD]
    let edge = [OA,OB,OC,OD,OE,OF,OG,OH,OI,OJ,OK,OL]


    for (let i=0;i<small_ring.length; i++)  {
        c.point(small_ring[i],"")
    }
    for (let i=0;i<middle_ring.length; i++)  {
        c.point(middle_ring[i],"")
    }
    for (let i=0;i<outer_ring.length; i++)  {
        c.point(outer_ring[i],"")
    }
    for (let i=0;i<edge.length; i++)  {
        c.point(edge[i],"")
    }
}
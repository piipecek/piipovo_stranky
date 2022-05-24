import {Cartesian_graph} from "./cartesian_graph.js"

let buttons = document.getElementsByClassName("cudlitka")
let generate_button = document.getElementById("generate")
let zmena_button = document.getElementById("zmena")
let buttons_div = document.getElementById("buttons")

for (let i=0;i<buttons.length;i++) {
    buttons[i].addEventListener("click", function() {button_pressed(buttons[i].id)})
}
generate_button.addEventListener("click", send)
zmena_button.addEventListener("click", display_parameters)

let result = {
    "force_desert": false,
    "adjacent_land": false,
    "ports": false,
    "adjacent_values": false,
    "unique_68": true,
    "adjacent_68": false
}

function display_parameters() {
    if (buttons_div.hidden) {
        buttons_div.hidden = false
        zmena_button.innerHTML = "Skrýt parametry"
    } else {
        buttons_div.hidden = true
        zmena_button.innerHTML = "Ukázat parametry"
    }
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
    document.getElementById("can").hidden = true
    buttons_div.hidden = true
    zmena_button.hidden = false
    zmena_button.innerHTML = "Ukázat parametry"
    generate_button.innerHTML = "Znovu generovat"
    $.ajax({
        data : {
            result: JSON.stringify(result)
        },
        type: "POST",
        url: "/visuals/catan"
    })
    .done(function(data) {
        document.getElementById("preloader").hidden = true
        document.getElementById("can").hidden = false
        draw_map(data)
    })
}

function draw_map(data) {
    // Ma nekolik casti: definice bodu, definice bodu pro jednotlivy dilky, kresleni dilku, kresleni okraju

    // Definice bodu
    data = JSON.parse(data)
    let c = new Cartesian_graph("map",1000,800,[500.5,400.5],70, true)
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

    // Definice potrebnejch skupin bodu
    let id_to_point = {
        0: [BA, BB, BC, BD, X, W],
        1: [BD, AA, AB, H, G, X],
        2: [AB, AC, AD, AE, I, H],
        3: [BA, W, V, U, AY, AZ],
        4: [W, X, G, A, F, V],
        5: [G, H, I, J, B, A],
        6: [I, AE, AF, AG, K, J],
        7: [U, T, AV, AW, AX, AY],
        8: [U,V,F,E,S,T],
        9: [A,B,C,D,E,F],
        10: [J,K,L,M,C,B],
        11: [AG, AH, AI, AJ, L, K],
        12: [T,S,R,AT,AU,AV],
        13: [E,D,P,Q,R,S],
        14: [D,C,M,N,O,P],
        15: [AJ, AK, AL, N,M,L],
        16: [R,Q,AQ,AR,AS,AT],
        17: [Q,P,O,AO,AP,AQ],
        18: [O,N,AL,AM,AN,AO]
    }

    let id_to_edge = {
        0: [OJ,OK,OL,AC,AB,AA,BD,BC,BB],
        1: [OL,OA,OB,AH,AG,AF,AE,AD,AC,],
        2: [OB,OC,OD,AM,AL,AK,AJ,AI,AH],
        3: [OD,OE,OF,AR,AQ,AP,AO,AN,AM],
        4: [OF,OG,OH,AW,AV,AU,AT,AS,AR],
        5: [OH,OI,OJ,BB,BA,AZ,AY,AX,AW]
    }

    // vykresovani dilku
    for (let i=0;i<data["tiles"].length;i++) {
        let barva
        let body = id_to_point[data["tiles"][i]["id"]]
        if (data["tiles"][i]["type"] == "ovce") {
            barva = "limegreen"
        } else if (data["tiles"][i]["type"] == "obili") {
            barva = "gold"
        } else if (data["tiles"][i]["type"] == "drevo") {
            barva = "forestgreen"
        } else if (data["tiles"][i]["type"] == "kamen") {
            barva = "grey"
        } else if (data["tiles"][i]["type"] == "cihly") {
            barva = "#C65D3A"
        } else if (data["tiles"][i]["type"] == "zlodej") {
            barva = "orange"
        }
        c.n_gon(body, barva, "black")

        //vykreslovani cisla uprostred
        let center = [0,0]
        for (let i=0;i<body.length;i++) {
            center[0]+=body[i][0]/6
            center[1]+=body[i][1]/6
        }
        if (data["tiles"][i]["type"] == "zlodej") {
            
        } else {
            c.circle(center, 0.3, true, "white", "white")
        }
        
        let value = data["tiles"][i]["value"]

        if ([2,12].includes(value)) {
            c.ctx.font = '20px arial';
            c.ctx.fillStyle = "black"
        } else if ([3,11].includes(value)) {
            c.ctx.font = '22px arial';
            c.ctx.fillStyle = "black"    
        } else if ([4,10].includes(value)) {
            c.ctx.font = '27px arial';
            c.ctx.fillStyle = "black"    
        } else if ([5,9].includes(value)) {
            c.ctx.font = '30px arial';
            c.ctx.fillStyle = "black"    
        } else if ([6,8].includes(value)) {
            c.ctx.font = '35px arial';
            c.ctx.fillStyle = "red"    
        } else {
            continue
        }

        c.ctx.textAlign = "center"
        c.ctx.textBaseline = "middle"
        c.ctx.fillText(String(value), c.rx(center[0]), c.ry(center[1]))

    }

     // kreslim porty jako kolecka, jejichz stred se pocita takhle
     function stred_portu_jako_fce_dvou_bodu_nejbliz(bod1, bod2) {
        let vec12 = [bod2[0]-bod1[0], bod2[1]-bod1[1]]
        let a = vec12[0]
        let b = vec12[1]
        let velikost_vec12 = Math.sqrt(a**2+b**2)
        let dst = velikost_vec12*(2/3)
        let alpha = Math.acos(a/velikost_vec12)
        if (bod2[1] < bod1[1]) {
            alpha = Math.PI*2-alpha
        }
        let ceix = bod1[0] + dst*Math.cos(alpha+Math.PI/6)
        let ceypsilon = bod1[1] + dst*Math.sin(alpha+Math.PI/6)
        return [ceix, ceypsilon]
    }

    // vykreslovani kraju
    for (let i=0;i<data["edges"].length; i++) {
        c.n_gon(id_to_edge[i], "dodgerblue", "black")

        let barva
        if (data["edges"][i] == "ovce") {
            barva = "limegreen"
        } else if (data["edges"][i] == "obili") {
            barva = "gold"
        } else if (data["edges"][i] == "drevo") {
            barva = "forestgreen"
        } else if (data["edges"][i] == "kamen") {
            barva = "grey"
        } else if (data["edges"][i] == "cihly") {
            barva = "#C65D3A"
        } else if (data["edges"][i] == null) {
            continue
        }    
        
        let id_to_related_points = {
            0: [[BD,AA], [AA,AB]],
            1: [[AE,AF], [AF,AG]],
            2: [[AJ,AK], [AK,AL]],
            3: [[AO,AP], [AP,AQ]],
            4: [[AT,AU], [AU,AV]],
            5: [[AY,AZ], [AZ,BA]]
        }
        
        if (["drevo", "kamen"].includes(data["edges"][i])) {
            c.circle(stred_portu_jako_fce_dvou_bodu_nejbliz(id_to_related_points[i][0][0],id_to_related_points[i][0][1]),0.25,true, barva, true, "black")
        } else if (["obili", "ovce", "cihly"].includes(data["edges"][i])) {
            c.circle(stred_portu_jako_fce_dvou_bodu_nejbliz(id_to_related_points[i][1][0],id_to_related_points[i][1][1]),0.25,true, barva, true, "black")
        }
    }
}
import {Cartesian_graph} from "./cartesian_graph.js"

function trig() {
    let b1 = document.getElementById("uvod")
    let b2 = document.getElementById("trojuhelnik")
    let b3 = document.getElementById("vlna")
    let b4 = document.getElementById("funkce")
    let b5 = document.getElementById("kartez")
    let t1 = document.getElementById("uvod_text")
    let t2 = document.getElementById("trojuhelnik_text")
    let t3 = document.getElementById("vlna_text")
    let t4 = document.getElementById("funkce_text")
    let t5 = document.getElementById("kartez_text")
    b1.addEventListener("click", uvod)
    b2.addEventListener("click", trojuhelnik)
    b3.addEventListener("click", vlna)
    b4.addEventListener("click", funkce)
    b5.addEventListener("click", kartez)

    
    function uvod() {
        t1.hidden = false
        t2.hidden = true
        t3.hidden = true
        t4.hidden = true
        t5.hidden = true
    }

    function trojuhelnik() {
        t1.hidden = true
        t2.hidden = false
        t3.hidden = true
        t4.hidden = true
        t5.hidden = true
        let c1 = new Cartesian_graph("trojuhelnik1", 500, 400, [250.5, 200.5], 50, true)

        let A = [-3,-2]
        let B = [2,-2]
        let C = [2,2]
        c1.point(A,"A")
        c1.point(B,"B")
        c1.point(C,"C")
        c1.two_point_line_segment(A,B,"")
        c1.two_point_line_segment(B,C,"")
        c1.two_point_line_segment(C,A,"")
        c1.angle(A,B,[3,-3],"")

    }

    function vlna() {
        t1.hidden = true
        t2.hidden = true
        t3.hidden = false
        t4.hidden = true
        t5.hidden = true
        let c = new Cartesian_graph("vlna_canvas", 1000, 800, [500.5, 400.5], 100)
        let A = [-1,1]
        c.two_point_line(A, [-3,0], "p1", "SW")
        c.point(A, "A")
        c.point([-3,0],"S")
        c.point([1,2], "T")
        c.point([2,2.5],"U")
        c.vector(A, [2,1],"v1","SE",1,)
        c.vector(A, [2,1],"","", 1.5)
        c.vector([-1,1],[-2,-1],"","")

    }

    function funkce() {
        t1.hidden = true
        t2.hidden = true
        t3.hidden = true
        t4.hidden = false
        t5.hidden = true
        let c = new Cartesian_graph("funkce_canvas", 1000, 800, [500.5, 400.5], 100)
        let A = [-1,1]
        let B = [3,3]
        let N = [2,-1]
        c.point(A, "A")
        c.point(B, "B")
        c.point(N, "N")
        c.vector(A,[2,1],"v1", "SE")
        c.vector(A, [-1,2], "n1", "SE")
        c.two_point_line(A,B,"p1", "SW")
    }

    function kartez() {
        t1.hidden = true
        t2.hidden = true
        t3.hidden = true
        t4.hidden = true
        t5.hidden = false
        let c = new Cartesian_graph("kartez_canvas", 1000, 800, [500.5, 400.5], 100)
        c.two_point_line([-1,1],[3,3],"p1", "SW")
    }

    uvod()
}

trig()


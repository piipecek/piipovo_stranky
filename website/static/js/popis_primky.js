import {Cartesian_graph} from "./cartesian_graph.js"

function primka() {
    let b1 = document.getElementById("vektor")
    let b2 = document.getElementById("vazany_vektor")
    let b3 = document.getElementById("param")
    let b4 = document.getElementById("general")
    let b5 = document.getElementById("slope")
    let t1 = document.getElementById("vektor_text")
    let t2 = document.getElementById("vazany_vektor_text")
    let t3 = document.getElementById("param_text")
    let t4 = document.getElementById("general_text")
    let t5 = document.getElementById("slope_text")
    let c = new Cartesian_graph("param_primka", 1000, 800, [500.5, 400.5], 100)
    b1.addEventListener("click", vektor)
    b2.addEventListener("click", vazany_vektor)
    b3.addEventListener("click", param)
    b4.addEventListener("click", general)
    b5.addEventListener("click", slope)

    
    function vektor() {
        t1.hidden = false
        t2.hidden = true
        t3.hidden = true
        t4.hidden = true
        t5.hidden = true

        c.clear()
        c.vector([1.5, 2.3],[2,1], "v1")
        c.vector([-3,1],[2,1], "v1")
        c.vector([0,0],[2,1], "v1")
        c.vector([-3,-3],[2,1], "v1")

    }

    function vazany_vektor() {
        t1.hidden = true
        t2.hidden = false
        t3.hidden = true
        t4.hidden = true
        t5.hidden = true

        c.clear()
        let A = [-1,1]
        c.point(A, "A")
        c.vector(A, [2,1], "v1")

    }

    function param() {
        t1.hidden = true
        t2.hidden = true
        t3.hidden = false
        t4.hidden = true
        t5.hidden = true

        c.clear()
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

    function general() {
        c.clear()
        let A = [-1,1]
        let B = [3,3]
        let N = [2,-1]
        c.point(A, "A")
        c.point(B, "B")
        c.point(N, "N")
        c.vector(A,[2,1],"v1", "SE")
        c.vector(A, [-1,2], "n1", "SE")
        c.two_point_line(A,B,"p1", "SW")
        t1.hidden = true
        t2.hidden = true
        t3.hidden = true
        t4.hidden = false
        t5.hidden = true
    }

    function slope() {
        c.clear()
        c.two_point_line([-1,1],[3,3],"p1", "SW")
        t1.hidden = true
        t2.hidden = true
        t3.hidden = true
        t4.hidden = true
        t5.hidden = false
    }

    vektor()
}

primka()


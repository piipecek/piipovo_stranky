import {Cartesian_graph} from "./cartesian_graph.js"

let c = new Cartesian_graph("param_primka", 1000, 800)
let A = [2,3]
let B = [-1,1]
c.axes([500.5, 400.5], 100)
c.point(A, "A")
c.point(B, "B", "NW")
c.point([2,1],"C","NE")
c.two_point_line(B, A, "p1")
c.vector([1,-1], [3,-2], "v1", "NW", 1)
c.vector([1,-1], [3,-2], "v2","NW",1.25)

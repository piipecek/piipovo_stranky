import {Cartesian_graph} from "./cartesian_graph.js"

let c = new Cartesian_graph("ppr0_1", 1000, 800, [500.5,400.5],100)

c.axes(true, true, true, false)
c.point([-2,-2],"B","NW",true)
c.two_point_line([-2,-2],[2,3],"p","SE")
c.two_point_line_segment([-2,-2],[3,-3],"k","SE")
c.vector([-2,3],[2,-3],"v","NE",1.5)
c.n_gon([[0,0],[1,0],[1,1],[0,1]],"green","green")
c.circle([0,0],4,false, "",true, "red")
c.angle([3,3],[3,1],[1,3])
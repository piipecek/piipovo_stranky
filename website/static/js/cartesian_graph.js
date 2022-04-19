class Cartesian_graph {
    // id: id elementu v DOM
    constructor(id, width, height, pxorigin, pxstep) {
        this.node = document.getElementById(id)
        this.ctx = this.node.getContext("2d")
        this.width = width
        this.height = height
        this.node.width = this.width
        this.node.height = this.height
        this.pxorigin = pxorigin
        this.px_step = pxstep
        this.axes()
    }

    clear() {
        this.ctx.clearRect(0,0,this.width, this.height)
        this.axes()
    }

    rx(num) {
        //real coords -> [0,0] vrátí origin
        return num*this.px_step + this.originX
    }

    ry (num) {
        return this.originY- num * this.px_step
    }

    axes() {
        this.originX = this.pxorigin[0]
        this.originY = this.pxorigin[1]
        console.log(this.pxorigin, this.width, this.height)
        this.axis_margin = 10
        this.label_offset = 10
        this.tick_size = 5
        this.ctx.strokeStyle = "black"
        this.ctx.lineWidth = 1
        this.ctx.beginPath()
        this.ctx.moveTo(10, this.originY)
        this.ctx.lineTo(this.width-this.axis_margin, this.originY)
        this.ctx.moveTo(this.originX, this.axis_margin)
        this.ctx.lineTo(this.originX, this.height-this.axis_margin)
        this.ctx.stroke()

        this.ctx.font = "10px Arial"
        this.ctx.fillText("0", this.rx(0)-this.label_offset, this.ry(0)+this.label_offset)
        //prichazi hodne duplicate codu, protoze se mi nepovedlo udelat draw axisline funkci.
        //x+
        let pos = 0
        while (true) {
            pos += 1
            if (this.rx(pos) > this.width-this.axis_margin) {
                break
            }
            this.ctx.strokeStyle = "silver"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(pos), this.axis_margin)
            this.ctx.lineTo(this.rx(pos), this.height-this.axis_margin)
            this.ctx.stroke()
            this.ctx.strokeStyle = "black"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(pos), this.ry(0)+this.tick_size)
            this.ctx.lineTo(this.rx(pos), this.ry(0)-this.tick_size)
            this.ctx.stroke()
            this.ctx.fillText(String(pos), this.rx(pos)-this.label_offset, this.ry(0)+this.label_offset)

        }
        //x-
        pos = 0
        while (true) {
            pos -= 1
            if (this.rx(pos) < this.axis_margin) {
                break
            }
            this.ctx.strokeStyle = "silver"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(pos), this.axis_margin)
            this.ctx.lineTo(this.rx(pos), this.height-this.axis_margin)
            this.ctx.stroke()
            this.ctx.strokeStyle = "black"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(pos), this.ry(0)+this.tick_size)
            this.ctx.lineTo(this.rx(pos), this.ry(0)-this.tick_size)
            this.ctx.stroke()
            this.ctx.fillText(String(pos), this.rx(pos)-this.label_offset, this.ry(0)+this.label_offset)

        }
        //y+
        pos = 0
        while (true) {
            pos += 1
            if (this.ry(pos) < this.axis_margin) {
                break
            }
            this.ctx.strokeStyle = "silver"
            this.ctx.beginPath()
            this.ctx.moveTo(this.axis_margin, this.ry(pos))
            this.ctx.lineTo(this.width-this.axis_margin, this.ry(pos))
            this.ctx.stroke()
            this.ctx.strokeStyle = "black"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(0)+this.tick_size, this.ry(pos))
            this.ctx.lineTo(this.rx(0)-this.tick_size, this.ry(pos))
            this.ctx.stroke()
            this.ctx.fillText(String(pos), this.rx(0)-this.label_offset, this.ry(pos)+this.label_offset)

        }
        //y-
        pos = 0
        while (true) {
            pos -= 1
            if (this.ry(pos) > this.width - this.axis_margin) {
                break
            }
            this.ctx.strokeStyle = "silver"
            this.ctx.beginPath()
            this.ctx.moveTo(this.axis_margin, this.ry(pos))
            this.ctx.lineTo(this.width-this.axis_margin, this.ry(pos))
            this.ctx.stroke()
            this.ctx.strokeStyle = "black"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(0)+this.tick_size, this.ry(pos))
            this.ctx.lineTo(this.rx(0)-this.tick_size, this.ry(pos))
            this.ctx.stroke()
            this.ctx.fillText(String(pos), this.rx(0)-this.label_offset, this.ry(pos)+this.label_offset)

        }
    }

    point(tuple,label, labelpos = "SE", draw_mark  = true) {
        // label = nazev bodu, labelpos = {NE, SE, SW, NW} - pozice názvu, drawmark = boolean
        let x = tuple[0]
        let y = tuple[1]
        if (draw_mark){
            this.point_size = 3
            this.ctx.strokeStyle = "green"
            this.ctx.lineWidth = "2"
            this.ctx.beginPath()
            this.ctx.moveTo(this.rx(x)-this.point_size, this.ry(y)+this.point_size)
            this.ctx.lineTo(this.rx(x)+this.point_size, this.ry(y)-this.point_size)
            this.ctx.moveTo(this.rx(x)+this.point_size, this.ry(y)+this.point_size)
            this.ctx.lineTo(this.rx(x)-this.point_size, this.ry(y)-this.point_size)
            this.ctx.stroke()
        }

        this.ctx.font = "15px Arial"
        let label_offset = 15
        if (labelpos == "NE") {
            this.ctx.fillText(String(label), this.rx(x)+label_offset, this.ry(y)-label_offset)
        } else if (labelpos == "SE") {
            this.ctx.fillText(String(label), this.rx(x)+label_offset, this.ry(y)+label_offset)
        } else if (labelpos == "SW") {
            this.ctx.fillText(String(label), this.rx(x)-label_offset, this.ry(y)+label_offset)
        } else if (labelpos == "NW") {
            this.ctx.fillText(String(label), this.rx(x)-label_offset, this.ry(y)-label_offset)
        }


    }

    two_point_line(A, B, label, labelpos) {
        let edge_x_plus = (this.width-this.originX-this.axis_margin)/this.px_step //jaká hodnta x v mém systému je na kraji render distance
        let edge_x_minus = (-this.originX+this.axis_margin)/this.px_step
        let edge_y_plus = (this.originY-this.axis_margin)/this.px_step
        let edge_y_minus = ( -this.height + this.originY + this.axis_margin)/this.px_step
        let a = (A[1]-B[1])
        let b = (B[0]-A[0])
        let c = A[0]*B[1] - B[0]*A[1]
        let Nprusecik
        let Eprusecik
        let Sprusecik
        let Wprusecik
        if (b==0) {
            Nprusecik = null
            Sprusecik = null
        } else {
            Nprusecik = (-c-b*edge_y_plus)/a
            Sprusecik = (-c-b*edge_y_minus)/a
        }
        if (a==0) {
            Wprusecik = null
            Eprusecik = null
        } else {
            Wprusecik = (-c-a*edge_x_minus)/b
            Eprusecik = (-c-a*edge_x_plus)/b
        }

        //zjistim, zda kazdej z tech 4 pruseciku je na platne nebo daleko. podle toho vyberu ty dva body
        // ruzny <= a < jsu kvuli tomu, kdyz by to prochazelo presne rohem
        let result = []
        if (edge_x_minus <= Nprusecik && Nprusecik <= edge_x_plus) {
            result.push([Nprusecik, edge_y_plus])
        }
        if (edge_x_minus <= Sprusecik && Sprusecik <= edge_x_plus) {
            result.push([Sprusecik, edge_y_minus])
        }
        if (edge_y_minus < Eprusecik && Eprusecik < edge_y_plus) {
            result.push([edge_x_plus, Eprusecik])
        }
        if (edge_y_minus < Wprusecik && Wprusecik < edge_y_plus) {
            result.push([edge_x_minus, Wprusecik])
        }

        this.ctx.strokeStyle = "blue"
        this.ctx.lineWidth = "1"
        this.ctx.beginPath()
        this.ctx.moveTo(this.rx(result[0][0]), this.ry(result[0][1]))
        this.ctx.lineTo(this.rx(result[1][0]), this.ry(result[1][1]))
        this.ctx.stroke()
        this.point(result[0], label, labelpos, false)

    }

    vector(point_tuple, direction_tuple, label = "", labelpos = "SE", multiplier = 1) {
        // direction tuple je vektor, point tuple je jeho uvazani na misto
        //multiplier = 1 -> vektor je velkeej jako direction tuple
        let alpha
        if (direction_tuple[1] > 0) {
            alpha = Math.acos( direction_tuple[0] / Math.sqrt(  Math.pow(direction_tuple[0],2) + Math.pow(direction_tuple[1],2)  ) )
        } else {
            alpha = -Math.acos( direction_tuple[0] / Math.sqrt(  Math.pow(direction_tuple[0],2) + Math.pow(direction_tuple[1],2)  ) )
        }
        let arrow_size = 10
        let arrow_angle = Math.PI/6
        let endx = point_tuple[0] + direction_tuple[0]*multiplier
        let endy = point_tuple[1] + direction_tuple[1]*multiplier

        this.ctx.strokeStyle = "red"
        this.ctx.lineWidth = "2"
        this.ctx.beginPath()
        this.ctx.moveTo(this.rx(point_tuple[0]), this.ry(point_tuple[1]))
        this.ctx.lineTo(this.rx(endx), this.ry(endy))
        this.ctx.lineTo(this.rx(endx) + arrow_size*Math.cos(alpha + Math.PI - arrow_angle), this.ry(endy) - arrow_size*Math.sin(alpha+Math.PI-arrow_angle))
        this.ctx.moveTo(this.rx(endx), this.ry(endy))
        this.ctx.lineTo(this.rx(endx) + arrow_size*Math.cos(alpha + Math.PI + arrow_angle), this.ry(endy) - arrow_size*Math.sin(alpha+Math.PI+arrow_angle))
        this.ctx.stroke()
        this.point([point_tuple[0] + direction_tuple[0]*multiplier/2, point_tuple[1] + direction_tuple[1]*multiplier/2], label, labelpos, false)
    }
}

export {Cartesian_graph}
class Cartesian_graph {
    // id: id elementu v DOM
    constructor(id, width, height, pxorigin, pxstep) {
        this.node = document.getElementById(id)
        this.ctx = this.node.getContext("2d")
        this.ctx.textAlign = "center"
        this.ctx.textBaseline = "middle"
        this.width = width
        this.height = height
        this.node.width = this.width
        this.node.height = this.height
        this.pxorigin = pxorigin
        this.originX = this.pxorigin[0]
        this.originY = this.pxorigin[1]
        this.px_step = pxstep
        this.axis_margin = 10
    }

    clear() {
        this.ctx.clearRect(0,0,this.width, this.height)
    }

    rx(num) {
        //real coords -> [0,0] vrátí origin
        return num*this.px_step + this.originX
    }

    ry (num) {
        return this.originY- num * this.px_step
    }

    odchylka_vektoru_od_osy_x(tuple) {
        let alpha
        if (tuple[1] >= 0) {
            alpha = Math.acos( tuple[0] / Math.sqrt(  Math.pow(tuple[0],2) + Math.pow(tuple[1],2)  ) )
        } else {
            alpha = -Math.acos( tuple[0] / Math.sqrt(  Math.pow(tuple[0],2) + Math.pow(tuple[1],2)  ) )
            alpha = Math.PI*2-Math.acos( tuple[0] / Math.sqrt(  Math.pow(tuple[0],2) + Math.pow(tuple[1],2)  ) )

        }
        return alpha
    }


    axes(axes, ticks, labels, grid) {
        // axes, ticks, labels i grid jsou booleany
        // vykresluje se to v poradi grid, ticks, labels, axes
        this.label_offset = 13
        this.tick_size = 5
        // zjistim, jake se renderujou xvalues a yvalues
        let xvalues = [0]
        let yvalues = [0]
        let pos = 0
        while (true) {
            pos += 1
            if (this.rx(pos) > this.width-this.axis_margin) {
                break
            } else {
                xvalues.push(pos)
            }
        }
        pos = 0
        while (true) {
            pos -= 1
            if (this.rx(pos) < this.axis_margin) {
                break
            } else {
                xvalues.push(pos)
            }
        }
        pos = 0
        while (true) {
            pos += 1
            if (this.ry(pos) < this.axis_margin) {
                break
            } else {
                yvalues.push(pos)
            }
        }
        pos = 0
        while (true) {
            pos -= 1
            if (this.ry(pos) > this.height - this.axis_margin) {
                break
            } else {
                yvalues.push(pos)
            }
        }

        //grid:
        if (grid) {
            this.ctx.strokeStyle = "silver"
            this.ctx.lineWidth = 1
            for (let x of xvalues) {
                if (x == 0) {
                } else {
                    this.ctx.beginPath()
                    this.ctx.moveTo(this.rx(x), this.axis_margin)
                    this.ctx.lineTo(this.rx(x), this.height-this.axis_margin)
                    this.ctx.stroke()
                }
            }
            for (let y of yvalues) {
                if (y == 0) {
                } else {
                    this.ctx.beginPath()
                    this.ctx.moveTo(this.axis_margin, this.ry(y))
                    this.ctx.lineTo(this.width-this.axis_margin,this.ry(y))
                    this.ctx.stroke()
                }
            }
        }

        // ticks
        if (ticks) {
            this.ctx.strokeStyle = "black"
            this.ctx.lineWidth = 1
            for (let x of xvalues) {
                if (x == 0) {
                } else {
                    this.ctx.beginPath()
                    this.ctx.moveTo(this.rx(x), this.ry(0)-this.tick_size)
                    this.ctx.lineTo(this.rx(x), this.ry(0)+this.tick_size)
                    this.ctx.stroke()
                }
            }
            for (let y of yvalues) {
                if (y == 0) {
                } else {
                    this.ctx.beginPath()
                    this.ctx.moveTo(this.rx(0)-this.tick_size, this.ry(y))
                    this.ctx.lineTo(this.rx(0)+this.tick_size,this.ry(y))
                    this.ctx.stroke()
                }
            }
        }
        // labels
        if (labels) {
            this.ctx.font = "12px Arial"
            this.ctx.strokeStyle = "black"
            for (let x of xvalues) {
                this.ctx.fillText(String(x), this.rx(x)-this.label_offset, this.ry(0)+this.label_offset)
            }
            for (let y of yvalues) {
                if (y==0) {

                } else {
                    this.ctx.fillText(String(y), this.rx(0)-this.label_offset, this.ry(y)+this.label_offset)
                }
            }
        }
        // axes
        if (axes) {
            this.ctx.strokeStyle = "navy" //lol prostě black nefunguje
            this.ctx.lineWidth = 1
            this.ctx.beginPath()
            this.ctx.moveTo(this.axis_margin, this.ry(0))
            this.ctx.lineTo(this.width-this.axis_margin, this.ry(0))
            this.ctx.moveTo(this.rx(0), this.axis_margin)
            this.ctx.lineTo(this.rx(0), this.height-this.axis_margin)
            this.ctx.stroke()
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

    two_point_line(A, B, label="", labelpos="") {
        let edge_x_plus = (this.width-this.originX-this.axis_margin)/this.px_step //jaká hodnta x v mém systému je na kraji render distance
        let edge_x_minus = (-this.originX+this.axis_margin)/this.px_step
        let edge_y_plus = (this.originY-this.axis_margin)/this.px_step
        let edge_y_minus = ( -this.height + this.originY + this.axis_margin)/this.px_step
        let a = (A[1]-B[1])
        let b = (B[0]-A[0])
        let c = A[0]*B[1] - B[0]*A[1] // ax+by+c=0

        let Nprusecik = (-c-b*edge_y_plus)/a //hodnota [Nprusecik, edge_y_plus]
        let Sprusecik = (-c-b*edge_y_minus)/a
        let Wprusecik = (-c-a*edge_x_minus)/b
        let Eprusecik = (-c-a*edge_x_plus)/b

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

    two_point_line_segment(A,B,label="",labelpos="") {
        this.ctx.strokeStyle = "black"
        this.ctx.lineWidth = "1"
        this.ctx.beginPath()
        this.ctx.moveTo(this.rx(A[0]),this.ry(A[1]))
        this.ctx.lineTo(this.rx(B[0]),this.ry(B[1]))
        this.ctx.stroke()
        this.point(B, label, labelpos, false)

    }

    vector(point_tuple, direction_tuple, label = "", labelpos = "SE", multiplier = 1) {
        // direction tuple je vektor, point tuple je jeho uvazani na misto
        //multiplier = 1 -> vektor je velkeej jako direction tuple
        let alpha = this.odchylka_vektoru_od_osy_x(direction_tuple)
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

    n_gon(points_array, color, border_color) {
        this.ctx.strokeStyle=border_color
        this.ctx.lineWidth = "2"
        this.ctx.fillStyle = color
        this.ctx.beginPath()
        this.ctx.moveTo(this.rx(points_array[0][0]), this.ry(points_array[0][1]))
        for (let i=1;i<points_array.length; i++) {
            this.ctx.lineTo(this.rx(points_array[i][0]), this.ry(points_array[i][1]))
        }
        this.ctx.closePath()
        this.ctx.stroke()
        this.ctx.fill()
    }

    circle(tuple, r, dofill, color, doborder, border_color) {
        this.ctx.strokeStyle=border_color
        this.ctx.lineWidth = "1"
        this.ctx.fillStyle = color
        this.ctx.beginPath()
        this.ctx.arc(this.rx(tuple[0]),this.ry(tuple[1]), r*this.px_step, 0, Math.PI*2)
        if (dofill) {
            this.ctx.fill()
        }
        if (doborder) {
            this.ctx.stroke()
        }
    }

    angle(startPoint, center, endPoint, label) {
        let start_rad = this.odchylka_vektoru_od_osy_x([startPoint[0]-center[0], startPoint[1]-center[1]])
        let end_rad = this.odchylka_vektoru_od_osy_x([endPoint[0]-center[0], endPoint[1]-center[1]])
        
        this.ctx.strokeStyle = "red"
        this.ctx.lineWidth = "1"
        this.ctx.beginPath()
        console.log(end_rad)
        this.ctx.arc(this.rx(center[0]), this.ry(center[1]), 0.7*this.px_step, start_rad, end_rad, true)
        this.ctx.stroke()
    }
}

export {Cartesian_graph}
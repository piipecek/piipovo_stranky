// constants
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const polomer_element = document.getElementById("polomer");
const rychlost_element = document.getElementById("rychlost")
const pocet_ryb_element = document.getElementById("pocet_ryb");
const width = 0.9 * window.innerWidth;
const height = 0.9 * window.innerHeight;
canvas.width = width;
canvas.height = height;


// parameters
let r = parseInt(polomer_element.value)
let n = parseInt(pocet_ryb_element.value)
let v = parseInt(rychlost_element.value)
let color = "red"


// other declarations
let ryby = []
let req;


// updates
function changed_polomer() {
    r=parseInt(polomer_element.value)
}
function changed_rychlost() {
    v=parseInt(rychlost_element.value)
}
function changed_pocet_ryb() {
    n = parseInt(pocet_ryb_element.value)
    cancelAnimationFrame(req)
    ctx.clearRect(0,0,width,height)
    ryby = []
    create_ryby()
    update()
}


// code
class Ryba {
    constructor(x, y, dx, dy) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
    }
    draw() {
        ctx.beginPath()
        ctx.fillStyle = color
        ctx.arc(this.x, this.y, r, 0, Math.PI*2)
        ctx.fill()
    }
    move() {
        if (this.x + r > width || this.x - r < 0) {
            this.dx *= -1 
        }
        if (this.y + r > height || this.y - r < 0) {
            this.dy *= -1
        }


        this.x += this.dx*v
        this.y += this.dy*v
        this.draw()
    }
}

function update() {
    ctx.clearRect(0,0,width, height);
    for (let i=0;i<n;i++) {
        ryby[i].move()
    }
    req = requestAnimationFrame(update)
}

function create_ryby() {
    for (let i=0; i<n; i++) {
        x = Math.random()*width
        y = Math.random()*height
        phi = Math.random()*Math.PI*2
        dx = Math.cos(phi)
        dy = Math.sin(phi)
        ryby.push(new Ryba(x,y,dx,dy))
    }
}


//MAIN
create_ryby()
update()

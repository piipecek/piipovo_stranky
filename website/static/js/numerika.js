let a_range = document.getElementById("a_range")
let b_range = document.getElementById("b_range")

a_range.addEventListener("input", function() {document.getElementById("a_value").innerHTML =  a_range.value})
b_range.addEventListener("input", function() {document.getElementById("b_value").innerHTML =  b_range.value})

let canvas = document.getElementById("axb_rovnice")
let ctx = canvas.getContext("2d")

function draw_axb() {
    ctx.fillStyle = "Black"
    ctx.beginPath()
    ctx.moveTo(10,250)
    ctx.lineTo(490,250)
    ctx.moveTo(20,10)
    ctx.lineTo(20,490)


    ctx.stroke()
}

draw_axb()
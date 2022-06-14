import httpGet from "./httpGet.js"

document.getElementById("logs").innerHTML = JSON.parse(httpGet("/send_admin/logs"))

const email = document.getElementById("email")
const password = document.getElementById("password")
const password_confirm = document.getElementById("password_confirm")
const button = document.getElementById("btn")
const form = document.getElementById("form")

button.addEventListener("click", validate_form)

function validate_form() {
    if (form.reportValidity()) {
        if (password.value.length < 7) {
            alert("Heslo musí být minimálně 8 znaků dlouhé")
        } else {
            if (password.value == password_confirm.value) {
                form.submit()
            } else {
                alert("Hesla se neschodují, ověřte to prosím.")
            }
        }
    }
}
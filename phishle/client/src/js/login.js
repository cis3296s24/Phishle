const login = document.getElementById("login");
const register = document.getElementById("register");
const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");
const regUsername = document.getElementById("regUsername");
const regPassword = document.getElementById("regPassword");
const regPassword2 = document.getElementById("regPassword2");

login.addEventListener("submit", e => {
    e.preventDefault();
    validateLogin();
});

register.addEventListener("submit", e => {
    e.preventDefault();
    validateRegister();
});

function setError(element, message){
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');
    errorDisplay.innerText = message;
    inputControl.classList.add("error");
    inputControl.classList.remove("success");
}

function setSuccess(element){
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector(".error");
    errorDisplay.innerText = "";
    inputControl.classList.add("success");
    inputControl.classList.remove("error");
}

function validateLogin(){
    const username = loginUsername.value.trim();
    const password = loginPassword.value.trim();
    if(username === ""){
        setError(loginUsername, "Username cannot be empty");
    }else{
        setSuccess(loginUsername);
    }
    if(password.length > 7){
        setSuccess(loginPassword);
    }else{
        setError(loginPassword, "Password must be at least 8 characters long");
    }
}

function validateRegister(){
    const username = regUsername.value.trim();
    const password1 = regPassword.value.trim();
    const password2 = regPassword2.value.trim();
    if(username === ""){
        setError(regUsername, "Username cannot be empty");
    }else{
        setSuccess(regUsername);
    }
    if(password1.length > 7){
        setSuccess(regPassword);
    }else{
        setError(regPassword, "Password must be at least 8 characters long");
    }
    if(password2 == password1){
        setSuccess(regPassword2);
    }else{
        setError(regPassword2, "Password must match original password");
    }
}
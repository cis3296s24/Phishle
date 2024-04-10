const login = document.getElementById("login");
const register = document.getElementById("register");
const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");
const regUsername = document.getElementById("regUsername");
const regPassword = document.getElementById("regPassword");
const regPassword2 = document.getElementById("regPassword2");
const loginInformation = new Map();

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
    userValid = false;
    passValid = false;
    if(loginInformation.has(username)){
        setSuccess(loginUsername);
        userValid = true;
    }else{
        setError(loginUsername, "Username is not valid");
    }
    if(loginInformation.get(username) == password){
        setSuccess(loginPassword);
        passValid = true;
    }else{
        setError(loginPassword, "Password is incorrect");
    }
    if(userValid && passValid){
        alert("logged in as " + username);
    }
}

function validateRegister(){
    const username = regUsername.value.trim();
    const password1 = regPassword.value.trim();
    const password2 = regPassword2.value.trim();
    userValid = false;
    pass1Valid = false;
    pass2Valid = false;
    if(username === ""){
        setError(regUsername, "Username cannot be empty");
    }else{
        setSuccess(regUsername);
        userValid = true;
    }
    if(password1.length > 7){
        setSuccess(regPassword);
        pass1Valid = true;
    }else{
        setError(regPassword, "Password must be at least 8 characters long");
    }
    if(password2 == password1){
        setSuccess(regPassword2);
        pass2Valid = true;
    }else{
        setError(regPassword2, "Password must match original password");
    }
    if(userValid && pass1Valid && pass2Valid){
        loginInformation.set(username, password1);
        alert("Registerd user: " + username);
    }
}
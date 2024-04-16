const { Sequelize, DataTypes } = require('sequelize');
const login = document.getElementById("login");
const register = document.getElementById("register");
const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");
const regUsername = document.getElementById("regUsername");
const regPassword = document.getElementById("regPassword");
const regPassword2 = document.getElementById("regPassword2");

// Database connection setup
const sequelize = new Sequelize('mysql://phishle:phishlepasswd@localhost/phishle_database');

// Define User model
const User = sequelize.define('User', {
    UserID: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    Username: { type: DataTypes.STRING(50), allowNull: false, unique: true },
    Password: { type: DataTypes.STRING(100), allowNull: false },
    PlayStreak: { type: DataTypes.INTEGER, defaultValue: 0 },
    WinStreak: { type: DataTypes.INTEGER, defaultValue: 0 },
    TotalWins: { type: DataTypes.INTEGER, defaultValue: 0 },
    TotalLosses: { type: DataTypes.INTEGER, defaultValue: 0 }
});

login.addEventListener("submit", e => {
    e.preventDefault();
    validateLogin();
});

register.addEventListener("submit", e => {
    e.preventDefault();
    validateRegister();
});

// Synchronize the models with the database
async function initializeDatabase() {
    await sequelize.sync();
}

// Function to validate login credentials
async function validateLogin() {  
    const username = loginUsername.value.trim();
    const password = loginPassword.value.trim();
    const user = await User.findOne({ where: { Username: username } });
    return user && user.Password === password;
}

// Function to validate registration
async function validateRegister() {
    const username = regUsername.value.trim();
    const password1 = regPassword.value.trim();
    const password2 = regPassword2.value.trim();
    let userValid = false;
    let pass1Valid = false;
    let pass2Valid = false;
    
    if (username === "") {
        setError(regUsername, "Username cannot be empty");
    } else if (await User.findOne({ where: { Username: username } })) {
        setError(regUsername, "Username is already taken");
    } else {
        setSuccess(regUsername);
        userValid = true;
    }
    
    if (password1.length > 7) {
        setSuccess(regPassword);
        pass1Valid = true;
    } else {
        setError(regPassword, "Password must be at least 8 characters long");
    }
    
    if (password2 === password1) {
        setSuccess(regPassword2);
        pass2Valid = true;
    } else {
        setError(regPassword2, "Password must match original password");
    }
    
    if (userValid && pass1Valid && pass2Valid) {
        // Create new user in the database
        try {
            await User.create({ Username: username, Password: password1 });
            alert("Registered user: " + username);
        } catch (error) {
            console.error("Error registering user:", error);
            // Handle error appropriately
        }
    }
}

module.exports = { initializeDatabase, validateLogin };
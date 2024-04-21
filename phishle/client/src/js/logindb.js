// This JavaScript code snippet will help users to enter login/register data and send it as JSON.
document.addEventListener("DOMContentLoaded", function() {
    // Add event listener for login button
    document.getElementById("loginbtn").addEventListener("click", function() {
        const username = document.getElementById("loginUsername").value;
        const password = document.getElementById("loginPassword").value;
        
        fetch('http://localhost:5000/userlogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({Username: username, Password: password}),
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert("Login successful!");
            } else {
                alert("Login failed!");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Add event listener for register button
    document.getElementById("registerbtn").addEventListener("click", function() {
        const username = document.getElementById("regUsername").value;
        const password = document.getElementById("regPassword").value;
        const password2 = document.getElementById("regPassword2").value;

        
        fetch('http://localhost:5000/userregister', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({Username: username, Password: password, Password2: password2}),
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert("Registration successful!");
            } else {
                alert("Registration failed!");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
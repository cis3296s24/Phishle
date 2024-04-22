document.addEventListener("DOMContentLoaded", function() {

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
                sessionStorage.setItem("username", username)
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
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert("Registration successful!");
            } else {
                alert("Registration failed: " + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert("Failed to connect to the server. Please check your connection and try again.");
        });
    });
    
});
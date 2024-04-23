function fetchLatestSetId() {
    return fetch('http://localhost:5000/latest_set_id')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
        })
        .then(data => {
            return data.latest_set_id;
        })
        .catch(error => {
            console.error('Error fetching latest set ID:', error);
            return null;
        });
}

function fetchEmails(setId) {
    fetch(`http://localhost:5000/play/${setId}`)
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
    })
    .then(emails => {
        const container = document.getElementById('emailList');
        container.innerHTML = ''; // Clear existing content
        emails.forEach(email => {
            container.appendChild(createEmailHtml(email));
        });
    })
    .catch(error => {
        console.error('Error fetching emails:', error);
    });
}

function createEmailHtml(email) {
    const emailContainer = document.createElement('div');
    emailContainer.className = 'email-container';

    emailContainer.onclick = function() {
        if (sessionStorage.getItem("hasPlayed") === "true") {
            alert("You have already played this game.");
            disableAllEmailContainers();
            return; 
        }

        verifyPhishing(email.set_id, email.email_id);

        sessionStorage.setItem("hasPlayed", "true");
        disableAllEmailContainers();
    };

    const emailHeader = document.createElement('div');
    emailHeader.className = 'email-header';
    emailHeader.innerHTML = `
        <span class="email-from"><strong>From:</strong> ${email.from_email}</span>
        <span class="email-to"><strong>To:</strong> ${email.to_email}</span>
        <span class="email-subject"><strong>Subject:</strong> ${email.subject}</span>
    `;
    emailContainer.appendChild(emailHeader);

    const emailBody = document.createElement('div');
    emailBody.className = 'email-body';
    emailBody.innerHTML = `<p>${email.body}</p>`;
    emailContainer.appendChild(emailBody);

    const emailClosing = document.createElement('div');
    emailClosing.className = 'email-closing';
    emailClosing.innerHTML = `<p>${email.closing}</p>`;
    emailContainer.appendChild(emailClosing);

    const emailAttachment = document.createElement('div');
    emailAttachment.className = 'email-attachment';
    emailAttachment.innerHTML = email.attachment && email.attachment !== 'none' ?
        `<p><strong>Attachment:</strong> ${email.attachment}</p>` :
        '<p><strong>Attachment:</strong> None</p>';
    emailContainer.appendChild(emailAttachment);

    const emailLink = document.createElement('div');
    emailLink.className = 'email-link';
    emailLink.innerHTML = email.link && email.link !== 'none' ?
        `<p><strong>Link:</strong> <a href="${email.link}" target="_blank">Click here</a></p>` :
        '<p><strong>Link:</strong> None</p>';
    emailContainer.appendChild(emailLink);
     
    if (email.link && email.link !== 'none') {
        emailLink.querySelector('a').addEventListener('click', function(event) {
            event.stopPropagation(); 
        });
    }

    return emailContainer;
}

function disableAllEmailContainers() {
    const containers = document.querySelectorAll('.email-container');
    containers.forEach(container => {
        container.style.opacity = '0.6'; 
        container.style.pointerEvents = 'none'; 
    });
}

function verifyPhishing(setId, emailId) {
    fetch(`http://localhost:5000/verify_phishing/${setId}/${emailId}`)
        .then(response => response.json())
        .then(result => {
            const feedbackElement = document.getElementById('feedback');
            if (!feedbackElement) {
                console.error('Feedback element not found in the document.');
                return; 
            }
            
            phishingResult = result.is_phishing ? 'Safetly identified phishing email' : 'Got HOOKED by an attacker';

            const username = sessionStorage.getItem("username");

            const endpoint = result.is_phishing ? '/updateStreak' : '/resetStreak';

            console.log("fucntion: " + endpoint)

            fetch(`http://localhost:5000${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ Username: username }) 
            });
  
            getFeedback(setId, emailId)
                .then(feedback => {
                    feedbackElement.innerText = feedback;
                    showModal(result.is_phishing);
                });
        })
        .catch(error => {
            console.error('Error during phishing verification:', error);
        });
}

function getFeedback(setId, emailId){
    return fetch(`http://localhost:5000/verify_phishing/${setId}/${emailId}/feedback`)
        .then(response => response.json())
        .then(data => {
            return data.feedback; 
        })
        .catch(error => {
            console.error('Error fetching feedback:', error);
            return 'Error fetching feedback'; 
        });
}

function showModal(isPhishing) {
    const modal = document.getElementById('feedbackModal');
    const closeButton = document.querySelector('.close');
    
    modal.style.display = 'block';
    feedback.style.color = isPhishing ? 'green' : 'red';

    updateButtonVisibility();
}

let latestSetId = null;
async function initializePage() {
    latestSetId = await fetchLatestSetId();

    if (latestSetId !== null) {
        fetchEmails(latestSetId);
    }
}

document.getElementById('copyToClipboard').addEventListener('click', function() {
    if (latestSetId !== null && phishingResult !== null) {
        const shareText = `Phishle #${latestSetId}. Result: ${phishingResult}`;
        navigator.clipboard.writeText(shareText).then(function() {
            alert("Copied to Clipboard: " + shareText);
            console.log('Copying to clipboard was successful!');
        }, function(err) {
            console.error('Could not copy text to clipboard: ', err);
        });
    } else {
        console.error('Set ID or result not available.');
    }
});

function showModalOnFirstVisit() {
    var hasVisited = sessionStorage.getItem("hasVisited");
    if (!hasVisited) {
        var instructionsModal = document.getElementById('instructionsModal');
        instructionsModal.style.display = 'block';
        sessionStorage.setItem("hasVisited", "true");
    }

    updateButtonVisibility();

}

function modalCloseHandlers() {
    var closeInstructionModal = document.querySelector('#instructionsModal .close');
    closeInstructionModal.onclick = function() {
        var instructionsModal = document.getElementById('instructionsModal');
        instructionsModal.style.display = 'none';
    }

    var closeFeedbackModal = document.querySelector('#feedbackModal .close');
    if (closeFeedbackModal) {  
        closeFeedbackModal.onclick = function() {
            var feedbackModal = document.getElementById('feedbackModal');
            feedbackModal.style.display = 'none';
        }
    }

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    }
}

function updateButtonVisibility() {
    const username = sessionStorage.getItem("username");

    if (username) {
        $("#loginFeedback").hide();
        $("#profileFeedback").show();
        $("#loginInstructions").hide();
        $("#profileInstructions").show();
    } else {
        $("#loginFeedback").show();
        $("#profileFeedback").hide();
        $("#loginInstructions").show();
        $("#profileInstructions").hide();
    }
}


document.addEventListener('DOMContentLoaded', function() {
    initializePage();

    showModalOnFirstVisit();

    modalCloseHandlers();
    
    updateButtonVisibility();

})

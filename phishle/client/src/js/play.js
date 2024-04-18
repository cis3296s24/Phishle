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
            console.log('Fetched latest set ID:', data.latest_set_id);
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

    const verifyButton = document.createElement('button');
    verifyButton.innerText = 'Verify Phishing';
    verifyButton.onclick = function() { verifyPhishing(email.set_id, email.email_id); };
    emailContainer.appendChild(verifyButton);

    return emailContainer;
}

function verifyPhishing(setId, emailId) {
    fetch(`http://localhost:5000/verify_phishing/${setId}/${emailId}`)
        .then(response => response.json())
        .then(result => {
            const feedbackElement = document.getElementById('feedback');
            const buttons = document.querySelectorAll('button');

            buttons.forEach(button => {
                button.disabled = true;
            });

            if (result.is_phishing) {
                feedbackElement.innerText = 'Correct! This email is a phishing attempt.';
                feedbackElement.style.color = 'green';
            } else {
                feedbackElement.innerText = 'Incorrect. This email is not a phishing attempt.';
                feedbackElement.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error during phishing verification:', error);
        });
}
async function initializePage() {
    const latestSetId = await fetchLatestSetId();

    if (latestSetId !== null) {
        fetchEmails(latestSetId);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
})

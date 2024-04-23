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

async function initializePage() {
    const latestSetId = await fetchLatestSetId();

    if (latestSetId !== null) {
        const footerElement = document.getElementById('footer');
        footerElement.innerText = 'No. ' + latestSetId;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
})

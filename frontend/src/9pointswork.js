document.addEventListener('DOMContentLoaded', () => {
    const statusElement = document.getElementById('health-status');

    fetch('/api/v1/health')
        .then(response => response.json())
        .then(data => {
            statusElement.textContent = 'Status: ' + data.status.toUpperCase();
        })
        .catch(error => {
            statusElement.textContent = 'Status: Error';
            console.error('Chyba: ', error);
        });
});
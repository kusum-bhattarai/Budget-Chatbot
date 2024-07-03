function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value;
    if (!message) return;

    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<div><strong>You:</strong> ${message}</div>`;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
    .then(response => response.json())
    .then(data => {
        messagesDiv.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
        input.value = '';
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}

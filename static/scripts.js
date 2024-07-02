document.getElementById('chat-form').addEventListener('submit', async function(event){
    event.preventDefault();
    const message=document.getElementById('message').value;
    const responseDiv=document.getElementById('response');

    const response=await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({message})
    });
    
    const data=await response.json();
    responseDiv.innerHTML+=`<p><strong>You:</strong> ${message}</p><p><strong>Bud:</strong> ${data.response}</p>`;
    document.getElementById('message').value='';
    responseDiv.scrollTop=responseDiv.scrollHeight;
});
const chatToggle = document.getElementById('chatToggle');
const chatWidget = document.getElementById('chatWidget');
const closeChat = document.getElementById('closeChat');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

// Toggle chat widget
chatToggle.addEventListener('click', () => {
    chatWidget.style.display = chatWidget.style.display === 'none' || chatWidget.style.display === '' ? 'block' : 'none';
});

// Close button
closeChat.addEventListener('click', () => {
    chatWidget.style.display = 'none';
});

// Send message
sendBtn.addEventListener('click', async () => {
    const msg = userInput.value.trim();
    if (!msg) return;

    appendMessage(msg, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';

    // Send message to Django backend
    try {
        const response = await fetch('/chat_api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ message: msg }),
        });

        const data = await response.json();
        appendMessage(data.reply, 'bot');
    } catch (error) {
        appendMessage('Error: Unable to connect to the server.', 'bot');
    }
});

// Enter key send
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
    }
});

function appendMessage(text, sender) {
    const wrapper = document.createElement('div');
    wrapper.className = `d-flex flex-row justify-content-${sender === 'user' ? 'end' : 'start'} mb-3`;

    const bubble = document.createElement('div');
    bubble.className = `p-2 ${sender === 'user' ? 'me-2 sender-message-field text-white bg-primary' : 'ms-2 bot-message-field bg-secondary text-white'} rounded`;
    bubble.innerHTML = `<p class="medium m-0">${text}</p>`;

    if (sender === 'user') {
        wrapper.appendChild(bubble);
        wrapper.innerHTML += `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp" alt="User" style="width: 40px; height: 40px; margin: 5px;">`;
    } else {
        wrapper.innerHTML = `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp" alt="Bot" style="width: 40px; height: 40px; margin: 5px;">`;
        wrapper.appendChild(bubble);
    }

    chatMessages.appendChild(wrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
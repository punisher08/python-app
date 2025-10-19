const chatToggle = document.getElementById('chatToggle');
const chatWidget = document.getElementById('chatWidget');
const closeChat = document.getElementById('closeChat');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');
const languageSelect = document.getElementById('languageSelect');

let sessionId = null;

// -------------------------
// Load previous conversation
// -------------------------
async function loadConversation() {
    try {
        const response = await fetch('/assistant/get_conversation/');
        const data = await response.json();

        // check for new session or expired session
        if (!sessionId || sessionId !== data.session_id) {
            console.warn('🕒 New chat session started or previous session expired.');
            sessionId = data.session_id;
            chatMessages.innerHTML = ''; // clear old messages
            appendMessage('Hi there! How can I help you today?', 'bot');
            return;
        }

        // normal flow: load existing conversation
        chatMessages.innerHTML = ''; // clear existing messages before loading
        if (!data.conversation || data.conversation.length === 0) {
            appendMessage('Hi there! How can I help you today?', 'bot');
            return;
        }

        data.conversation.forEach(msg => {
            appendMessage(msg.message, msg.sender);
        });

        scrollToBottom();
    } catch (error) {
        console.error('Failed to load conversation:', error);
        appendMessage('⚠️ Unable to load chat history.', 'bot');
    }
}


function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// -------------------------
// Toggle chat widget
// -------------------------
chatToggle.addEventListener('click', () => {
    const isHidden =
        chatWidget.style.display === 'none' || chatWidget.style.display === '';
    chatWidget.style.display = isHidden ? 'block' : 'none';

    if (isHidden && chatMessages.children.length === 0) {
        loadConversation();
    }

    if (isHidden) scrollToBottom();
});

// Close button
closeChat.addEventListener('click', () => {
    chatWidget.style.display = 'none';
});

// -------------------------
// Send message
// -------------------------
sendBtn.addEventListener('click', async () => {
    const msg = userInput.value.trim();
    const language = languageSelect ? languageSelect.value : 'English';
    if (!msg) return;

    appendMessage(msg, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';

    const typingEl = appendTypingIndicator();

    try {
        const response = await fetch('/assistant/chat_api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message: msg,
                language: language,
                session_id: sessionId,
            }),
        });

        if (!response.ok) {
            const text = await response.text();
            typingEl.remove();
            appendMessage(`⚠️ Server error (${response.status}): ${text}`, 'bot');
            return;
        }

        const data = await response.json();
        typingEl.remove();

        if (data.session_id) sessionId = data.session_id;
        const replyText = data.reply.trim();
        if (data.reply)
            if (replyText.length > 400)
                appendMessage(replyText, 'bot');
            else 
                await typeMessage(replyText, 'bot');
        else appendMessage('⚠️ No reply received from server.', 'bot');
    } catch (error) {
        typingEl.remove();
        console.error('Chat API Error:', error);
        appendMessage('❌ Error: Unable to connect to the server.', 'bot');
    }
});

// Enter key send
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
    }
});

// -------------------------
// Sanitize HTML for safety
// -------------------------
function sanitizeHTML(html) {
    const tpl = document.createElement('template');
    tpl.innerHTML = html;

    tpl.content.querySelectorAll('script').forEach(s => s.remove());

    tpl.content.querySelectorAll('*').forEach(el => {
        [...el.attributes].forEach(attr => {
            const name = attr.name.toLowerCase();
            const val = attr.value || '';
            if (name.startsWith('on')) el.removeAttribute(attr.name);
            if (/^\s*javascript:/i.test(val)) el.removeAttribute(attr.name);
        });
    });

    return tpl.innerHTML;
}

// -------------------------
// Append message (bot or user)
// -------------------------
function appendMessage(text, sender) {
    const wrapper = document.createElement('div');
    wrapper.className = `d-flex flex-row justify-content-${
        sender === 'user' ? 'end' : 'start'
    } mb-3`;

    const bubble = document.createElement('div');
    bubble.className = `p-2 ${
        sender === 'user'
            ? 'me-2 sender-message-field text-white bg-primary'
            : 'ms-2 bot-message-field bg-secondary text-white'
    } rounded`;

    if (sender === 'user') {
        const contentDiv = document.createElement('div');
        contentDiv.className = 'medium m-0';
        contentDiv.textContent = text;
        bubble.appendChild(contentDiv);

        wrapper.appendChild(bubble);
        const userImg = document.createElement('img');
        userImg.src = 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp';
        userImg.alt = 'User';
        userImg.style.width = '40px';
        userImg.style.height = '40px';
        userImg.style.margin = '5px';
        wrapper.appendChild(userImg);
    } else {
        const safeHTML = sanitizeHTML(String(text));
        bubble.innerHTML = `<div class="medium m-0">${safeHTML}</div>`;

        const botImg = document.createElement('img');
        botImg.src = 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp';
        botImg.alt = 'Bot';
        botImg.style.width = '40px';
        botImg.style.height = '40px';
        botImg.style.margin = '5px';
        wrapper.appendChild(botImg);

        wrapper.appendChild(bubble);
    }

    chatMessages.appendChild(wrapper);
    scrollToBottom();
    return bubble;
}

// -------------------------
// Typing indicator
// -------------------------
function appendTypingIndicator() {
    const typingWrapper = document.createElement('div');
    typingWrapper.className = 'd-flex flex-row justify-content-start mb-3';
    typingWrapper.innerHTML = `
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp" 
            alt="Bot" style="width: 40px; height: 40px; margin: 5px;">
        <div class="typing-indicator ms-2 p-2 rounded bg-secondary text-white">
            <span></span><span></span><span></span>
        </div>`;
    chatMessages.appendChild(typingWrapper);
    scrollToBottom();
    return typingWrapper;
}

// -------------------------
// Get CSRF Token
// -------------------------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// -------------------------
// Auto-load conversation on page load
// -------------------------
document.addEventListener('DOMContentLoaded', loadConversation);

function sanitizeHTML(html) {
    const tpl = document.createElement('template');
    tpl.innerHTML = html;
    tpl.content.querySelectorAll('script').forEach(s => s.remove());
    tpl.content.querySelectorAll('*').forEach(el => {
        [...el.attributes].forEach(attr => {
            const name = attr.name.toLowerCase();
            const val = attr.value || '';
            if (name.startsWith('on') || /^\s*javascript:/i.test(val)) {
                el.removeAttribute(attr.name);
            }
        });
    });
    return tpl.innerHTML;
}

// Typing animation with HTML support
async function typeMessage(text, sender) {
    const bubble = appendMessage('', sender);
    const container = bubble.querySelector('.medium');

    // sanitize before rendering
    const safeHTML = sanitizeHTML(text);
    let temp = document.createElement('div');
    temp.innerHTML = safeHTML;
    const fullHTML = temp.innerHTML;

    // simulate typing by revealing chunks of HTML progressively
    let i = 0;
    while (i <= fullHTML.length) {
        container.innerHTML = fullHTML.substring(0, i);
        i++;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 10)); // speed
    }
}
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('question-input');
    const sendBtn = document.getElementById('send-btn');
    const messageList = document.getElementById('message-list');

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        input.value = '';
        sendBtn.disabled = true;

        const loadingId = appendLoading();

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text })
            });
            const data = await response.json();
            
            removeElement(loadingId);
            
            if (response.ok) {
                appendMessage(data.answer, 'bot');
            } else {
                appendMessage(`Error: ${data.detail}`, 'bot');
            }
        } catch (err) {
            removeElement(loadingId);
            appendMessage(`Error de red: ${err.message}`, 'bot');
        } finally {
            sendBtn.disabled = false;
            input.focus();
        }
    }

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.innerHTML = `<div class="bubble">${escapeHtml(text).replace(/\n/g, '<br>')}</div>`;
        messageList.appendChild(msgDiv);
        messageList.scrollTop = messageList.scrollHeight;
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot';
        msgDiv.id = id;
        msgDiv.innerHTML = `<div class="bubble loading">Pensando...</div>`;
        messageList.appendChild(msgDiv);
        messageList.scrollTop = messageList.scrollHeight;
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});

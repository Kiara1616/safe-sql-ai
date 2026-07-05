document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('question-input');
    const sendBtn = document.getElementById('send-btn');
    const messageList = document.getElementById('message-list');
    const providerSelect = document.getElementById('provider-select');

    async function sendMessage() {
        const text = input.value.trim();
        const provider = providerSelect.value;
        if (!text) return;

        appendUserMessage(text);
        input.value = '';
        sendBtn.disabled = true;
        input.disabled = true;

        const loadingId = appendLoading();

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text, provider: provider })
            });
            const data = await response.json();
            
            removeElement(loadingId);
            
            if (response.ok) {
                appendBotMessage(data);
            } else {
                appendError(`Error del Servidor: ${data.detail}`);
            }
        } catch (err) {
            removeElement(loadingId);
            appendError(`Error de conexión: Verifica que el backend esté encendido (${err.message})`);
        } finally {
            sendBtn.disabled = false;
            input.disabled = false;
            input.focus();
        }
    }

    function appendUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message user`;
        msgDiv.innerHTML = `<div class="bubble">${escapeHtml(text).replace(/\n/g, '<br>')}</div>`;
        messageList.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendBotMessage(data) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message bot`;
        
        let html = `<div class="bubble">`;
        
        // 1. Mensaje Natural
        html += `<div class="answer-text">${escapeHtml(data.answer).replace(/\n/g, '<br>')}</div>`;
        
        // 2. Acordeón SQL (si existe)
        if (data.sql && data.sql.trim() !== '') {
            html += `
                <div class="sql-accordion" onclick="this.classList.toggle('open')">
                    <div class="sql-accordion-header">
                        <div class="sql-accordion-header-title">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                            <span>Ver SQL Generado</span>
                        </div>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </div>
                    <div class="sql-accordion-content">${escapeHtml(data.sql)}</div>
                </div>
            `;
        }
        
        // 3. Tabla de Datos (si existe)
        if (data.data && Array.isArray(data.data) && data.data.length > 0) {
            html += `<div class="data-table-container"><table class="data-table">`;
            
            // Cabeceras
            const keys = Object.keys(data.data[0]);
            html += `<thead><tr>`;
            keys.forEach(k => html += `<th>${escapeHtml(k)}</th>`);
            html += `</tr></thead><tbody>`;
            
            // Filas
            data.data.forEach(row => {
                html += `<tr>`;
                keys.forEach(k => {
                    let val = row[k] !== null ? row[k] : 'NULL';
                    html += `<td>${escapeHtml(String(val))}</td>`;
                });
                html += `</tr>`;
            });
            html += `</tbody></table></div>`;
        }
        
        html += `</div>`;
        msgDiv.innerHTML = html;
        messageList.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendError(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message bot`;
        msgDiv.innerHTML = `<div class="bubble" style="border: 1px solid #ef4444; color: #fca5a5;">${escapeHtml(text)}</div>`;
        messageList.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot';
        msgDiv.id = id;
        msgDiv.innerHTML = `<div class="bubble"><div class="loading-dots"><span></span><span></span><span></span></div></div>`;
        messageList.appendChild(msgDiv);
        scrollToBottom();
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
    
    function scrollToBottom() {
        messageList.scrollTop = messageList.scrollHeight;
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});

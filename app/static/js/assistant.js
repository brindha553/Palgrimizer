/* ==========================================================================
   PALGRIM AI ASSISTANT DRAWER LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const triggerBtn = document.getElementById('assistantTriggerBtn');
    const drawer = document.getElementById('aiAssistantDrawer');
    const closeBtn = document.getElementById('closeAssistantBtn');
    const sendBtn = document.getElementById('sendAssistantMsgBtn');
    const inputField = document.getElementById('assistantInput');
    const messagesBox = document.getElementById('assistantMessages');
    const chipBtns = document.querySelectorAll('.prompt-chip');

    if (triggerBtn && drawer) {
        triggerBtn.addEventListener('click', () => {
            drawer.classList.toggle('active');
        });
    }

    if (closeBtn && drawer) {
        closeBtn.addEventListener('click', () => {
            drawer.classList.remove('active');
        });
    }

    if (sendBtn && inputField && messagesBox) {
        sendBtn.addEventListener('click', () => sendMessage());
        inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    chipBtns.forEach(chip => {
        chip.addEventListener('click', () => {
            const prompt = chip.getAttribute('data-prompt');
            if (inputField) {
                inputField.value = prompt;
                sendMessage();
            }
        });
    });

    async function sendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        // Append User Message
        appendMessage(text, 'user');
        inputField.value = '';

        // Context text from document editor if available
        let contextText = '';
        const originalTextEl = document.getElementById('originalTextContent');
        if (originalTextEl) contextText = originalTextEl.innerText;

        // Append Typing indicator
        const typingId = appendTypingIndicator();

        try {
            const res = await fetch('/api/assistant/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: text, context_text: contextText })
            });
            const data = await res.json();
            removeTypingIndicator(typingId);

            if (data.status === 'success') {
                appendMessage(data.reply, 'ai');
            } else {
                appendMessage("Sorry, I could not process your request.", 'ai');
            }
        } catch (e) {
            removeTypingIndicator(typingId);
            appendMessage("Error communicating with AI Assistant.", 'ai');
        }
    }

    function appendMessage(text, sender) {
        const bubble = document.createElement('div');
        bubble.className = `chat-bubble chat-bubble-${sender}`;
        bubble.innerHTML = text.replace(/\n/g, '<br>');
        messagesBox.appendChild(bubble);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function appendTypingIndicator() {
        const id = 'typing_' + Date.now();
        const bubble = document.createElement('div');
        bubble.id = id;
        bubble.className = 'chat-bubble chat-bubble-ai';
        bubble.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Thinking...';
        messagesBox.appendChild(bubble);
        messagesBox.scrollTop = messagesBox.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const welcomeScreen = document.getElementById('welcome-screen');
    const chatContainer = document.getElementById('chat-container');

    // Auto-focus input
    userInput.focus();

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        // Hide welcome screen on first message
        if (welcomeScreen && welcomeScreen.style.display !== 'none') {
            chatContainer.classList.add('chat-started');
        }

        // Add user message
        addMessage(message, 'user');
        userInput.value = '';

        // Disable input while loading
        setInputState(false);

        // Add loading indicator
        const loadingId = addLoadingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove loading indicator
            removeLoadingIndicator(loadingId);

            if (response.ok) {
                addMessage(data.response, 'bot');
            } else {
                const errorMessage = data && data.error ? data.error : 'Unknown server error';
                addMessage(`Error: ${errorMessage}. Please check your server or Vercel logs.`, 'bot');
                console.error('Error from server:', data);
            }
        } catch (error) {
            // Remove loading indicator
            removeLoadingIndicator(loadingId);
            addMessage('Network error. Please check your connection.', 'bot');
            console.error('Fetch error:', error);
        } finally {
            // Re-enable input
            setInputState(true);
            userInput.focus();
        }
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        // Convert newlines to <br> for display
        const textWithBreaks = text.replace(/\n/g, '<br>');
        messageDiv.innerHTML = textWithBreaks;

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function addLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.id = id;
        loadingDiv.classList.add('typing-indicator');

        loadingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;

        chatMessages.appendChild(loadingDiv);
        scrollToBottom();
        return id;
    }

    function removeLoadingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendBtn.disabled = !enabled;
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

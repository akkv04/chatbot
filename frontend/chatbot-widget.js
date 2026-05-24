(function () {
    const API_URL = "http://localhost:8000"; // Update this to your production backend URL

    // Inject CSS - Make sure this points to the correct location on your JBoss server
    // If you host the CSS in the same folder as the JS, you can use:
    // const scriptPath = document.currentScript.src;
    // const cssPath = scriptPath.substring(0, scriptPath.lastIndexOf("/")) + "/chatbot-widget.css";
    const styleLink = document.createElement("link");
    styleLink.rel = "stylesheet";
    styleLink.href = "chatbot-widget.css";
    document.head.appendChild(styleLink);

    // Create Container
    const container = document.createElement("div");
    container.id = "chatbot-container";
    document.body.appendChild(container);

    // Create Bubble
    const bubble = document.createElement("div");
    bubble.id = "chatbot-bubble";
    bubble.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2m0 14H6l-2 2V4h16v12z"/></svg>';
    container.appendChild(bubble);

    // Create Window
    const chatWindow = document.createElement("div");
    chatWindow.id = "chatbot-window";
    chatWindow.innerHTML = `
        <div id="chatbot-header">
            <h3>Assistant</h3>
            <button id="chatbot-close">&times;</button>
        </div>
        <div id="chatbot-messages">
            <div class="chatbot-message bot">Hello! How can I help you today?</div>
        </div>
        <div id="chatbot-input-area">
            <input type="text" id="chatbot-input" placeholder="Type a message...">
            <button id="chatbot-send">Send</button>
        </div>
    `;
    container.appendChild(chatWindow);

    const input = chatWindow.querySelector("#chatbot-input");
    const sendBtn = chatWindow.querySelector("#chatbot-send");
    const messages = chatWindow.querySelector("#chatbot-messages");
    const closeBtn = chatWindow.querySelector("#chatbot-close");

    // Toggle Window
    bubble.onclick = () => chatWindow.classList.add("open");
    closeBtn.onclick = () => chatWindow.classList.remove("open");

    // Add Message function
    function addMessage(text, type) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `chatbot-message ${type}`;
        msgDiv.textContent = text;
        messages.appendChild(msgDiv);
        messages.scrollTop = messages.scrollHeight;
        return msgDiv;
    }

    // Show Typing
    function showTyping() {
        const typing = document.createElement("div");
        typing.className = "chatbot-message bot typing-indicator";
        typing.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        messages.appendChild(typing);
        messages.scrollTop = messages.scrollHeight;
        return typing;
    }

    // Send logic
    async function sendMessage() {
        if (API_URL.includes("localhost") && window.location.hostname !== "localhost") {
            console.warn("Chatbot Warning: API_URL is set to localhost but you are accessing from a remote IP. Chatbot might not connect.");
        }

        const text = input.value.trim();
        if (!text) return;

        input.value = "";
        addMessage(text, "user");

        const typing = showTyping();

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000); // 15s timeout

            const response = await fetch(`${API_URL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) throw new Error("Server error");

            const data = await response.json();
            typing.remove();
            addMessage(data.answer, "bot");
        } catch (error) {
            typing.remove();
            let errorMessage = "Sorry, I'm having trouble connecting to the brain.";
            if (error.name === 'AbortError') errorMessage = "Response timed out. The brain is taking too long.";

            addMessage(errorMessage, "bot");
            console.error("Chat error:", error);
        }
    }

    sendBtn.onclick = sendMessage;
    input.onkeypress = (e) => { if (e.key === "Enter") sendMessage(); };
})();

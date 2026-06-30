// Get elements
const sendButton = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

// Send button click
sendButton.addEventListener("click", async function () {

    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    // Show user's message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";

    userMessage.innerHTML = `
        <div class="bubble">
            ${message}
        </div>
    `;

    chatBox.appendChild(userMessage);

    userInput.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    // Show typing message
    const typingMessage = document.createElement("div");

    typingMessage.className = "message bot";

    typingMessage.innerHTML = `
        <div class="icon">
            🤖
        </div>

        <div class="bubble">
            AI is typing...
        </div>
    `;

    chatBox.appendChild(typingMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    // Get CSRF token
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Send request
    const response = await fetch("/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    // Remove typing message
    typingMessage.remove();

    // Show AI reply
    const botMessage = document.createElement("div");

    botMessage.className = "message bot";

    botMessage.innerHTML = `
        <div class="icon">
            🤖
        </div>

        <div class="bubble">
            ${marked.parse(data.response)}
        </div>
    `;

    chatBox.appendChild(botMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

});
// Send message when Enter key is pressed
userInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendButton.click();

    }

});
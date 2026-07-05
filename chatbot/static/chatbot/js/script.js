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
        <button
            class="bookmark-btn"
            data-message-id=""
            title="Bookmark">

            <i class="fa-regular fa-bookmark"></i>

        </button>
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
        <button
            class="bookmark-btn"
            data-message-id="${data.assistant_message_id}"
            title="Bookmark">

            <i class="fa-regular fa-bookmark"></i>

        </button>
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
/* ===========================
   Search Chats
=========================== */

const searchInput = document.getElementById("search-chat");

if (searchInput) {

    searchInput.addEventListener("input", function () {

        const searchText = this.value.toLowerCase().trim();

        const chatItems = document.querySelectorAll(".chat-item");

        chatItems.forEach(function (chat) {

            const title = chat.getAttribute("data-title").toLowerCase();

            if (title.includes(searchText)) {

                chat.style.display = "block";

            } else {

                chat.style.display = "none";

            }

        });

    });

}

/* ===========================
   Bookmark Messages
=========================== */

document.addEventListener("click", async function (event) {

    const button = event.target.closest(".bookmark-btn");

    console.log("Bookmark button clicked");

    if (!button) return;

    const messageId = button.dataset.messageId;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    const response = await fetch("/bookmark/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },

        body: JSON.stringify({
            message_id: messageId
        })

    });

    const data = await response.json();

    const icon = button.querySelector("i");

    if (data.status === "saved") {

        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");

    }

    else if (data.status === "removed") {

        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");

    }
});
/* ===========================
   Theme Toggle
=========================== */

const themeBtn = document.getElementById("theme-btn");

// Apply saved theme
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    themeBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
}

themeBtn.addEventListener("click", function () {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

        themeBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';

    } else {

        localStorage.setItem("theme", "light");

        themeBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';

    }

});
/* ===========================
   Profile Dropdown
=========================== */

const profileBtn = document.getElementById("profile-btn");
const profileMenu = document.querySelector(".profile-menu");

if (profileBtn && profileMenu) {

    profileBtn.addEventListener("click", function (e) {

        e.stopPropagation();

        profileMenu.classList.toggle("active");

    });

    document.addEventListener("click", function () {

        profileMenu.classList.remove("active");

    });

}

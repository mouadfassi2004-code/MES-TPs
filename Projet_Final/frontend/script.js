const API_URL = "http://127.0.0.1:8000/chat";

window.addEventListener("DOMContentLoaded", function () {
    const student = localStorage.getItem("campusbot_student");

    if (!student) {
        window.location.href = "login.html";
        return;
    }

    const studentData = JSON.parse(student);
    const studentName = document.getElementById("studentName");

    if (studentName) {
        studentName.textContent = studentData.full_name;
    }
});

function logout() {
    localStorage.removeItem("campusbot_student");
    window.location.href = "login.html";
}

function addMessage(message, sender) {
    const chatBox = document.getElementById("chatBox");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    if (sender === "user") {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("bot-message");
    }

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = sender === "user" ? "ME" : "CB";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = message;

    if (sender === "user") {
        messageDiv.appendChild(bubble);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingMessage() {
    const chatBox = document.getElementById("chatBox");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "bot-message");
    messageDiv.setAttribute("id", "loadingMessage");

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = "CB";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = "CampusBot prépare une réponse...";

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoadingMessage() {
    const loadingMessage = document.getElementById("loadingMessage");

    if (loadingMessage) {
        loadingMessage.remove();
    }
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const userMessage = input.value.trim();

    if (userMessage === "") {
        return;
    }

    addMessage(userMessage, "user");
    input.value = "";

    addLoadingMessage();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage
            })
        });

        const data = await response.json();

        removeLoadingMessage();
        addMessage(data.bot_response, "bot");

    } catch (error) {
        removeLoadingMessage();
        addMessage(
            "Erreur de connexion avec le serveur. Vérifiez que le Chatbot Service est bien lancé.",
            "bot"
        );
    }
}

function sendQuickQuestion(question) {
    const input = document.getElementById("userInput");
    input.value = question;
    sendMessage();
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

let window_opened = true;
let visibilityCheckTimeout = setTimeout(checkVisibility, 1000);
let chatContainer = document.getElementById('chat-container');
document.addEventListener("visibilitychange", function () {
    clearTimeout(visibilityCheckTimeout);
    if (document.visibilityState === 'visible') {

        visibilityCheckTimeout = setTimeout(checkVisibility, 1000);
        window_opened = true;
    } else {

        window_opened = false;
    }
});
if (window_opened) {
    console.log('Вкладка активна');
} else {
    console.log('Вкладка неактивна');
}
document.getElementById("message-input").addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});


// const historySocket = new WebSocket('ws://127.0.0.1:8002/ws/history/');
//
// historySocket.onopen = function () {
//     console.log('HistorySocket connection established.');
//     requestHistory();
// };
// historySocket.onclose = function () {
//     console.log('HistorySocket connection closed.');
// };
//
//
// historySocket.onmessage = function (event) {
//     console.log('historySocket onmessage');
//     let data = JSON.parse(event.data);
//     console.log(data);
//     addMessageToChat(data.sender_name, data.message, data.type, data.status, data.id);
// };
//
// function requestHistory() {
//     historySocket.send(JSON.stringify({
//         'channel_name': receiver_id,
//         'receiver_name': receiver_name,
//         'sender_name': sender_name,
//         'sender_id': sender_id
//     }));
// }

const chatSocket = new WebSocket('ws://127.0.0.1:8002/ws/chat/');
chatSocket.onopen = function () {
    console.log('WebSocket connection established.');
    requestHistory();
};


chatSocket.onmessage = function (event) {
    console.log('onmessage');
    let data = JSON.parse(event.data);
    console.log(data.message);
    addMessageToChat(data.sender_name, data.message, data.type, data.status, data.id);
};


chatSocket.onclose = function () {
    console.log('WebSocket connection closed.');
};

function requestHistory() {
    chatSocket.send(JSON.stringify({
        'type': 'history',
        'message': '',
        'channel_name': receiver_id,
        'receiver_name': receiver_name,
        'sender_name': sender_name,
        'sender_id': sender_id,
    }));
}


function sendMessage() {
    let messageInput = document.getElementById('message-input');
    let message = messageInput.value.trim();
    if (receiver_id && message !== '') {
        chatSocket.send(JSON.stringify({
            'type': 'message',
            'message': message,
            'channel_name': receiver_id,
            'receiver_name': receiver_name,
            'sender_name': sender_name,
            'sender_id': sender_id
        }));
        messageInput.value = '';
    }
}


function isVisible(element) {
    let rect = element.getBoundingClientRect();
    let containerRect = chatContainer.getBoundingClientRect();

    return (
        rect.top >= containerRect.top &&
        rect.bottom <= containerRect.bottom
    );
}


function getUnreadVisibleMessageIds() {
    const unreadVisibleMessageIds = [];
    let messages = document.querySelectorAll('.message');
    messages.forEach(function (message) {
        // Проверяем, виден ли элемент и его data-read равно false
        if (isVisible(message) && message.getAttribute('data-read') === 'false' && message.classList.contains('receiver-message')) {
            unreadVisibleMessageIds.push(message.getAttribute('id'));
        }
    });
    if (unreadVisibleMessageIds.length > 0)
        return JSON.stringify({'type': 'read_report', 'read_ids': unreadVisibleMessageIds});
    else return null;
}

function checkVisibility() {
    let report = getUnreadVisibleMessageIds();
    console.log("Проверили видимость, отправили отчет о прочтении", report);

    if (report) {
        notifySocket.send(report);
    }

}

function setStatuses(read_ids) {
    console.log("Получилось передать в другое место");
    read_ids.forEach(function (id) {
        let message = document.getElementById(id);
        if (message) {
            message.setAttribute('data-read', 'true');
            message.style.fontWeight = 'normal';
        }
    });
}

chatContainer.addEventListener('scroll', function () {
    console.log("Крутим колесико")
    clearTimeout(visibilityCheckTimeout);
    visibilityCheckTimeout = setTimeout(checkVisibility, 1000);
});


// function sendReadReport() {
//     let messageInput = document.getElementById('message-input');
//     let message = messageInput.value.trim();
//
//     if (receiver_id && message !== '') {
//         chatSocket.send(JSON.stringify({
//             'type': 'chat_message',
//             'message': message,
//             'channel_name': receiver_id,
//             'receiver_name': receiver_name,
//             'sender_name': sender_name,
//             'sender_id': sender_id
//         }));
//         messageInput.value = '';
//     }
// }

function addMessageToChat(sender, message, type, status, id) {

    let messageElement = document.createElement('div');
    messageElement.classList.add('message');

    console.log(type)
    if (type === 'from_me') {

        messageElement.classList.add('sender-message');

    } else {
        messageElement.classList.add('receiver-message');
        const stringStatus = `${status}`;
        const stringId = `${id}`;
        messageElement.setAttribute('data-read', stringStatus);
        messageElement.setAttribute('id', stringId);
    }
    messageElement.innerHTML = '<span class="user">' + sender + '</span>: ' + message;
    messageElement.style.fontWeight = status === 'false' ? 'bold' : 'normal';
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    clearTimeout(visibilityCheckTimeout);
    visibilityCheckTimeout = setTimeout(checkVisibility, 1000);
}



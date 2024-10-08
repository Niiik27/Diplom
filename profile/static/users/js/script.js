function requestNumsUnreadByUsers() {
    if (window.socket && window.socket.readyState === WebSocket.OPEN) {
        window.socket.send(JSON.stringify({'type': 'from_client_read_num_unread_by_users'}));
    } else {
        console.error('WebSocket is not open. Ready state: ' + (window.socket ? window.socket.readyState : 'No socket'));
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    if (window.socket && window.socket.readyState === WebSocket.OPEN) {
        window.socket.send(JSON.stringify({'type': 'from_client_read_num_unread_by_users'}));
    } else {
        document.addEventListener('websocketOpen', requestNumsUnreadByUsers, {once: true});
    }
});


function addNewUnreadNumByUsers(counts) {
    for (let i = 0; i < counts.length; i++) {
        let user_data = counts[i];
        let user_id = user_data[0];
        let num_unreads = user_data[1];
        let user_item = `sender_${user_id}`
        console.log("Добавили непрочтенное", user_data);
        console.log("user_id", user_id);
        console.log("user_item", user_item);
        console.log("num_unreads", num_unreads);
        let usersContainer = document.getElementById(user_item);
        // let currentCount = parseInt(usersContainer.textContent);
        usersContainer.textContent = `Написать ${num_unreads}`;
    }

}


$(document).ready(function () {


    // Используем делегирование событий для разворачивания/сворачивания выпадающего списка
    $('#teamTable').on('click', '.select-header', function () {
        $(this).siblings(".select-options").toggle();
            $(this).toggleClass('active');

    });

    // При уводе мыши с области выпадающего списка, он скрывается
    $('#teamTable').on('mouseleave', '.select-wrapper', function () {
        $(this).find(".select-options").hide();
    $(this).find(".select-header").removeClass('active');

    });
});

// Полный URL страницы
const fullURL = window.location.href;
console.log('Full URL:', fullURL);

// Протокол (http или https)
const protocol = window.location.protocol;
console.log('Protocol:', protocol);

// Имя хоста (доменное имя или IP-адрес)
const hostname = window.location.hostname;
console.log('Hostname:', hostname);

// Порт (если указан)
const port = window.location.port;
console.log('Port:', port);

// Путь на сервере (часть URL после доменного имени)
const pathname = window.location.pathname;
console.log('Pathname:', pathname);

// Строка запроса (часть URL после ?)
const search = window.location.search;
console.log('Search:', search);

// Фрагмент (часть URL после #)
const hash = window.location.hash;
console.log('Hash:', hash);

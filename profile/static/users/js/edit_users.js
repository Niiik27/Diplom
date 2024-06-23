document.addEventListener('DOMContentLoaded', function() {
    // Функция для получения CSRF-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Устанавливаем CSRF-токен в заголовок
    const csrftoken = getCookie('csrftoken');

    // Обработчик для каждой кнопки "Сохранить"
    document.querySelectorAll('.save-btn').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            const row = document.getElementById(`row_${userId}`);

            // Собираем данные из формы
            const addressData = {};
            row.querySelectorAll(`[id^="address_${userId}_"]`).forEach(input => {
                const key = input.name;
                if (input.tagName.toLowerCase() === 'select') {
                    // addressData[key] = input.options[input.selectedIndex].text;
                    addressData[key] = input.selectedIndex;
                } else {
                    addressData[key] = input.value;
                }
            });
            const dict_socialLinks = {};
            row.querySelectorAll('input[name="social_link"]').forEach(input => {
                const socialNetwork = input.getAttribute('placeholder');
                const socialLink = input.value.trim(); // получаем значение ссылки
                if (socialLink) {
                    dict_socialLinks[socialNetwork] = socialLink;
                }
            });
            const list_socialLinks = [];
            row.querySelectorAll('input[name="social_link"]').forEach(input => {
                list_socialLinks.push(input.value.trim());
            });
            const data = {
                'user_id': userId,
                'photo_url': row.querySelector(`#img_${userId}`).value,
                'login': row.querySelector(`#login_${userId}`).value,
                'address': addressData,
                'phone_number': row.querySelector(`#phone_${userId}`).value,
                // 'status': row.querySelector(`#status_${userId}`).value,
                'status': row.querySelector(`#status_${userId}`).selectedIndex+1,
                'specializations': Array.from(row.querySelectorAll(`input[name="spec"]:checked`)).map(checkbox => checkbox.value),
                'permissions': Array.from(row.querySelectorAll(`input[name="allow"]:checked`)).map(checkbox => checkbox.value),
                'social_links_dict': dict_socialLinks,
                'social_links_list': list_socialLinks,
                'messengers': Array.from(row.querySelectorAll(`input[name="messenger"]:checked`)).map(checkbox => checkbox.value),
            };

            // Отправляем данные на сервер через AJAX
            fetch(`/profile/save_user/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Данные успешно сохранены');
                } else {
                    alert(`Ошибка при сохранении данных: ${data.error}`);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка при сохранении данных');
            });
        });
    });
});










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

// document.addEventListener('DOMContentLoaded', function() {
//     const selectElements = document.querySelectorAll('.st-sl');
//
//     selectElements.forEach(selectElement => {
//         selectElement.addEventListener('mouseover', function() {
//             selectElement.size = selectElement.options.length; // Раскрываем все опции
//         });
//
//         selectElement.addEventListener('mouseleave', function() {
//             selectElement.size = 16; // Скрываем опции при уходе мыши
//         });
//
//         selectElement.addEventListener('blur', function() {
//             selectElement.size = 1; // Скрываем опции при потере фокуса
//         });
//     });
// });

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

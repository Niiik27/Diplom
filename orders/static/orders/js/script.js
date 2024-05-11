$(document).ready(function () {
    $('[id^="sendButton_"]').click(function () {
        let button = $(this); // Сохраняем ссылку на кнопку
        let takeUrl = button.data('take-url'); // Получаем URL из атрибута data-take-url
        let token = button.data('token'); // Получаем токен из атрибута data-token
        let orderId = button.data('order-id'); // Получаем id
        console.log(takeUrl, orderId)

        let requestData = {
            orderId: orderId,
        };
        $.ajax({
            type: "POST",
            url: takeUrl,
            data: requestData,
            headers: {
                "X-CSRFToken": token
            },
            success: function (response) {
                console.log("Запрос успешно отправлен:", response);
                button.hide(); // Скрыть нажатую кнопку
                let newTextElement = $("<p>Заказ в работе</p>");
                button.after(newTextElement); // Добавить новый элемент после нажатой кнопки
            },
            error: function (xhr, status, error) {
                console.error("Произошла ошибка:", error);
            }
        });
    });
});

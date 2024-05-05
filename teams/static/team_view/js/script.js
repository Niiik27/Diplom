$(document).ready(function () {
    $(".sendButton").click(function () {
        // Получаем team_id из атрибута data-team-id кнопки, на которую нажали
        let teamId = $(this).data("team-id");

        let requestData = {
            team_id: teamId,
        };
        $.ajax({
            type: "POST",
            url: take_url,
            data: requestData,
            headers: {
                "X-CSRFToken": token
            },
            success: function (response) {
                console.log("Запрос успешно отправлен:", response);
                // Скрываем кнопку после успешного вступления
                $(this).hide();
                // Добавляем новый элемент с текстом
                let newTextElement = $("<p>Добро пожаловать в бригаду</p>");
                $(this).after(newTextElement);
            }.bind(this), // Привязываем контекст выполнения к кнопке
            error: function (xhr, status, error) {
                console.error("Произошла ошибка:", error);
            }
        });
    });
});

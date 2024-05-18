//Это для мастера
$(document).ready(function () {
        $("#sendButton").click(function () {
            let requestData = {
                customer_id: cust_id,
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
                    $("#sendButton").hide();
                    let newTextElement = $("<p>Заказ в работе</p>");
                    $("#sendButton").after(newTextElement);
                },
                error: function (xhr, status, error) {
                    console.error("Произошла ошибка:", error);
                }
            });
        });
    });
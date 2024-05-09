$(document).ready(function () {
    $("#addWorkerBtn").click(function () {
        let workersContainer = $("#workers");
        let newWorker = workersContainer.find('.worker').first().clone(true);

        // Изменяем имена полей ввода, добавляя уникальный индекс
        let newIndex = workersContainer.find('.worker').length;
        newWorker.find('select, input').each(function () {
            let currentId = $(this).attr('id');
            if (currentId) {
                $(this).attr('id', currentId + '_' + newIndex);
            }
            this.name = this.name.replace(/\d+/g, newIndex);
        });

        workersContainer.append(newWorker);
    });

    // Используем делегирование событий для разворачивания/сворачивания выпадающего списка
    $('#teamTable').on('click', '.select-header', function () {
        $(this).siblings(".select-options").toggle();
    });

    // При уводе мыши с области выпадающего списка, он скрывается
    $('#teamTable').on('mouseleave', '.select-wrapper', function () {
        $(this).find(".select-options").hide();
    });
});
document.getElementById('addRowBtn').addEventListener('click', function() {
    let newRow = document.getElementById('teamTable').getElementsByTagName('tbody')[0].getElementsByTagName('tr')[0].cloneNode(true);
    newRow.querySelectorAll('select').forEach(select => {
        select.selectedIndex = 0; // Сбросить выбор в списке выбора
    });
    newRow.querySelectorAll('input[type="text"], input[type="checkbox"]').forEach(input => {
        input.value = ''; // Очистить текстовые поля и снять все флажки у чекбоксов
        input.checked = false;
    });
    document.getElementById('teamTable').getElementsByTagName('tbody')[0].appendChild(newRow);
});

document.getElementById('saveBtn').addEventListener('click', function() {
    let tableData = [];
    let rows = document.getElementById('teamTable').getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        let cells = rows[i].getElementsByTagName('td');
        let rowData = {};
        for (let j = 0; j < cells.length; j++) {
            let input = cells[j].querySelector('select, input[type="text"], input[type="checkbox"]');
            let columnName = cells[j].getAttribute('data-column-name'); // Получаем имя колонки
            if (input) if (input.tagName === 'SELECT') {
                rowData[columnName] = input.options[input.selectedIndex].value;
            } else if (input.tagName === 'INPUT' && input.type === 'checkbox') {
                if (columnName === 'allowances') {
                    // Получаем все чекбоксы разрешений в ячейке и формируем список булевых значений
                    let allowances = cells[j].querySelectorAll('input[type="checkbox"]');
                    let allowancesList = [];
                    allowances.forEach(checkbox => {
                        allowancesList.push(checkbox.checked);
                    });
                    console.log(allowancesList);
                    rowData[columnName] = allowancesList;
                } else {
                    rowData[columnName] = input.checked;
                }
            } else {
                rowData[columnName] = input.value;
            }
        }
        tableData.push(rowData);
    }

    tableData.forEach(row => {
        if (row.allowances && Array.isArray(row.allowances)) {
            let selectedAllowances = [];
            row.allowances.forEach((allowance, index) => {
                if (allowance) {
                    selectedAllowances.push(index);
                }
            });
            selectedAllowances = selectedAllowances.map(value => value + 1);
            row.allowances = selectedAllowances;
        }
    });

console.log("tableData",tableData);
    // Отправить данные на сервер с помощью AJAX
    $.ajax({
        type: 'POST',
        url: taburl,
        data: { workers: JSON.stringify(tableData) },
        headers: {"X-CSRFToken": csrf_token},
        success: function(response) {
            console.log('Данные успешно отправлены на сервер:', response);
        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка:', error);
        }
    });
});


document.querySelectorAll('[id^="delRowBtn_"]').forEach(button => {
    button.addEventListener('click', function() {
        let rowId = this.id.split('_')[1];
        console.log("rowId",rowId)
console.log("delete_user_from_team",delete_user_from_team)
        // AJAX запрос для удаления
        $.ajax({
            type: 'POST',
            url: delete_user_from_team,
            data: {
                team_id: rowId,
            },
            headers: {"X-CSRFToken": csrf_token},
            success: function(response) {
                // Обработка успешного удаления
                console.log('Пользователь успешно удален из бригады:', response);
                // Удаление строки из таблицы
                document.querySelector(`#teamTable tr:nth-child(${rowId})`).remove();
            },
            error: function(xhr, status, error) {
                // Обработка ошибки удаления
                console.error('Произошла ошибка при удалении пользователя из бригады:', error);
            }
        });
    });
});
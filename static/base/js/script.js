//Скрипт для header
const notifySocket = new WebSocket('ws://127.0.0.1:8002/ws/notify/');

notifySocket.onopen = function () {
    console.log('notifySocket connection established.');
    const event = new CustomEvent('websocketOpen');
    document.dispatchEvent(event);
};
notifySocket.onclose = function () {
    console.log('notifySocket connection closed.');
};

notifySocket.onmessage = function (event) {
    console.log('Пришло оповещение');
    let data = JSON.parse(event.data);
    console.log(data);
    if (data.type === 'set_statuses') {
        console.log("incomingNotify", data);
        console.log("incomingNotify", data.statuses);
        setStatuses(data.statuses);
    } else if (data.type === 'total_messages') {
        addUnreadNum(data.num);
        console.log('Пришло уведомление о количестве сообщений', data.num, data.type);
    } else if (data.type === 'new_msg') {
        addNewUnreadNum(data.num);
        console.log('Пришло уведомление о новом сообщении', data.num, data.type);
    } else if (data.type === 'total_orders') {
        console.log('Пришло уведомление о всех ордерах', data.num);
        addTotalOrders(data.num);
    } else if (data.type === 'new_order') {
        console.log('Пришло уведомление о новом ордере', data.num);
        addNewOrder(data.num);
    } else if (data.type === 'total_teams') {
        console.log('Пришло уведомление о всех бригадах', data.num);
        addTotalTeams(data.num);
    } else if (data.type === 'new_team') {
        console.log('Пришло уведомление о новой бригаде', data.num);
        addNewTeam(data.num);
    } else if (data.type === 'team_complete') {
        console.log('Пришло уведомление об укомплектованности бригады', data.num);
        teamComplete(data.num);
    } else if (data.type === 'set_unread_nums_by_sender') {
        console.log('Уведомление о количестве непрочитанных по пользователям', data.num);
        addNewUnreadNumByUsers(data.unread_nums_by_sender);
    }

};
window.socket = notifySocket;
// function requestTotalNotify() {
//     notifySocket.send(JSON.stringify({'type': 'total'}));
// }

function addUnreadNum(count) {
    let usersContainer = document.getElementById('users');
    usersContainer.textContent = count;
}

function addNewUnreadNum(count) {
    let usersContainer = document.getElementById('users');
    let currentCount = parseInt(usersContainer.textContent);
    usersContainer.textContent = currentCount + count;
}

function addTotalOrders(count) {
    let usersContainer = document.getElementById('orders-total');
    usersContainer.textContent = count;
}

function addTotalTeams(count) {
    let usersContainer = document.getElementById('teams-total');
    usersContainer.textContent = count;
}

// hideBrigade();
// function hideBrigade(){
//     let usersContainer = document.getElementById('teams-total');
//     if(!usersContainer.textContent)
//     {
//         let usersContainer2 = document.getElementById('team-complete');
//         usersContainer2.textContent = "";
//     }
// }

function addNewOrder(count) {
    let usersContainer = document.getElementById('orders-total');
    let currentCount = parseInt(usersContainer.textContent);
    usersContainer.textContent = currentCount + count;
}

function addNewTeam(count) {
    console.log('Добавили новую команду', count);

    let usersContainer = document.getElementById('teams-total');
    let currentCount = parseInt(usersContainer.textContent);
    usersContainer.textContent = currentCount + count;
}

function teamComplete(count) {
    console.log('Бригада укомплектована', count);
    let usersContainer = document.getElementById('team-complete');
    switch (count) {
        case -1:
            usersContainer.textContent = "Нет бригады"
            break;
        case 0:
            usersContainer.textContent = "Бригада укомплектована"
            break;
        default:
            usersContainer.textContent = `О бригаде ${count}`
            break;
    }


    // if (count === 0) {
    //     usersContainer.textContent = "Бригада укомплектована"
    // } else if (usersContainer) {
    //     usersContainer.textContent = `О бригаде ${count}`
    // }
}


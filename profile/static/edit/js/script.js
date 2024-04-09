let img_link = document.getElementById("img_link");

function setImageUrl() {
    const link = img_link.value;
    let my_img = document.getElementById("profile_img");
    if (link) {
        my_img.alt = "Не получилось загрузить картинку";
        my_img.src = link;

    } else {
        my_img.alt = 'Вставте ссылку на картинку';
        my_img.src = "#";
    }
}


img_link.addEventListener("change", function () {
    setImageUrl();
});
// document.getElementById("img_link").addEventListener("focus", function(){setImageUrl();});
// document.getElementById("img_link").addEventListener("focusout", function(){setImageUrl();});
// document.getElementById("img_link").addEventListener("keydown", function(){setImageUrl();});
// document.getElementById("img_link").addEventListener("blur", function(){setImageUrl();});


// Форматирование телефона

const phoneInput = document.getElementById('phone');
// phoneInput.value = '+7('

// phoneInput.addEventListener('keypress', (event) => {
//     console.log(event.key)
//     if (parseInt(event.key)){
//         event.target.value=8
//     }
//    });


phoneInput.addEventListener('focus', (event) => {
    parsePhoneNumber(event);
});
phoneInput.addEventListener('focusout', (event) => {
    parsePhoneNumber(event);
});
phoneInput.addEventListener('keypress', (event) => {
    // +7(953) 986-31-65
    parsePhoneNumber(event)
});

function setStartVal(event) {
    const start = '+7(';
    if (!event.target.value.startsWith(start) || event.target.value.length < start.length) {
        event.target.value = start;
    } else {
        parsePhoneNumber(event);
    }
}

function parsePhoneNumber(event) {
    if (event.target.value.length > 16) {
        event.preventDefault();
    }

    let start = '+7';
    if (!event.target.value.startsWith(start) || event.target.value.length < start.length) {
        start+="(";
        event.target.value = start;
    } else {
        start+="(";
        const regexp = /\d/;
        if (!regexp.test(event.key)) {
            event.preventDefault();
        }
        let tmp = '';
        for (ch = 2; ch < 17; ch++) {
            if (parseInt(event.target.value[ch])) {
                if (tmp.length < 10) {
                    tmp += event.target.value[ch];
                } else {
                    break;
                }

            }

        }
        console.log(tmp);
        let res = '';
        for (let ch in tmp) {
            res += tmp[ch];
            if (res.length === 3) {
                res += ') ';
            } else if (res.length === 8) {
                res += '-';
            } else if (res.length === 11) {
                res += '-';
            }
        }
        console.log(res);
        event.target.value = start + res;
    }
}
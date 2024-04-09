/**
 Просмотр галереи
 Описание кода в проядке следования:
 Метод getImgPath нужен чтобы удалить из пути к миниатюре подкаталог tmb. тогда получится путь к основной картинке.
 Из описания метода следует что в миниатюры попадают уменьшенные картинки, апри выборе картинки она подгружается
 с сервера. По крайней мере такова задумка - экономия времени и трафика...
 Соответственно при получении картинки на сервере будет создаватья thumb...
 Метод get_date преобразует дату из какого то формата в русскоязычную
 Хотелось бы обойтись без него, но что то преобразует дату из sql в англоязычную строку, которую обратно потом
 не запихнуть, а значит, придется делать обратное форматирование, а раз такое дело, то не важно что форматировать
 по этому преобразую эту непонятную строку в русскую, а при редактировании инфо на сервере уже она
 преобразуется в формат даты для сохранения...
 Далее идет сама галерея. Код добывает поля картинки и миниатюр..При тыке на миниатюру происходит подгрузка нужной
 картинки, но без тыка должна подгрузиться картинка по умолчанию (первая)
 по этому код до обработчика занят этим и сбором нужных переменных, которые могут использоваться не только в
 галереи, но и в коде добавления, редактирования и удаления... может нужно добавить независимости каждому блоку
 но ножны ли эти функции без самой галереи?
 Блоки добавления, редактирования и удаления добавляют соответствующие кнопки в хедер. Решение временное,
 но нужно было кудато их добавить, что бы можно было поработать с функционалом
 Форма отправки имеет два скрытых поля - id картинки и режим отправки - редактирование,удаление, или новое
 сервер по ним понимает что нужно сделать
 */
function getImgPath(path) {
    const pathParts = path.split('/');
    const filteredPathParts = pathParts.filter(part => part !== 'tmb');
    return filteredPathParts.join('/');
}


function get_date(date) {
    let day_list = ['первое', 'второе', 'третье', 'четвёртое',
        'пятое', 'шестое', 'седьмое', 'восьмое',
        'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
        'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
        'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
        'двадцать первое', 'двадцать второе', 'двадцать третье',
        'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
        'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
        'тридцатое', 'тридцать первое'];
    let month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

    const months = {
        'Jan.': 'января',
        'Feb.': 'февраля',
        "March": 'марта',
        "April": 'апреля',
        "May": 'мая',
        "June": 'июня',
        "July": 'июля',
        "Aug.": 'августа',
        "Sept.": 'сентября',
        "Oct.": 'октября',
        "Nov.": 'ноября',
        "Dec.": 'декабря'
    };

    console.log(date)
    let date_list = date.split(',')
    let year = parseInt(date_list[1])
    console.log(year)
    let day_and_month = date_list[0].split(' ')
    let day = parseInt(day_and_month[1])
    console.log(day)
    let month = day_and_month[0]
    console.log(month)

    return (day_list[day - 1] + ' ' +
        months[month] + ' ' +
        year + ' года')

}

function get_format_date(date) {
    // date = 'второе октября 2023 года';
    let day_list = ['первое', 'второе', 'третье', 'четвёртое', 'пятое', 'шестое', 'седьмое', 'восьмое',
        'девятое', 'десятое', 'одиннадцатое', 'двенадцатое', 'тринадцатое', 'четырнадцатое', 'пятнадцатое',
        'шестнадцатое', 'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое', 'двадцать первое',
        'двадцать второе', 'двадцать третье', 'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
        'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое', 'тридцатое', 'тридцать первое'];
    let month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
        'октября', 'ноября', 'декабря'];

    let day_dict = {
        'первое': '01', 'второе': '02', 'третье': '03', 'четвёртое': '04', 'пятое': '05', 'шестое': '06',
        'седьмое': '07', 'восьмое': '08', 'девятое': '09', 'десятое': '10', 'одиннадцатое': '11', 'двенадцатое': '12',
        'тринадцатое': '13', 'четырнадцатое': '14', 'пятнадцатое': '15', 'шестнадцатое': '16', 'семнадцатое': '17',
        'восемнадцатое': '18', 'девятнадцатое': '19', 'двадцатое': '20', 'двадцать первое': '21',
        'двадцать второе': '22', 'двадцать третье': '23', 'двадацать четвёртое': '24', 'двадцать пятое': '25',
        'двадцать шестое': '26', 'двадцать седьмое': '27', 'двадцать восьмое': '28', 'двадцать девятое': '29',
        'тридцатое': '30', 'тридцать первое': '31'
    };
    let month_dict = {
        'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
        'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
    };

    let date_list = date.split(' ');
    let year = date_list[date_list.length - 2];
    let month_str = date_list[date_list.length - 3];
    let day_str = date_list.slice(0, date_list.length - 3).join(' ');
    let month = month_dict[month_str];
    let day = day_dict[day_str];

    let date_str = `${year}-${month}-${day}`;

    return date_str;

}

// console.log(get_format_date('двадцать второе октября 2023 года'))
/**Блок галереи*/
const mainView = document.getElementById('img_view');
console.log("mainView");
console.log(mainView);

if (mainView) {
    const mainBlock = mainView.children;
// const mainImage = mainBlock.namedItem('main-image');
// mainImage.hidden="hidden"

    const mainDescription = mainBlock.namedItem('descriptions').children;
    const mainImage_title = mainDescription.namedItem('img_title').children.item(0);
    const mainImage_desc = mainDescription.namedItem('img_desc').children.item(0);
    const mainImage_date = mainDescription.namedItem('img_date').children.item(0);
    const mainImage_urls = mainDescription.namedItem('img_urls').children.item(0);

    const mainImage_id = mainDescription.namedItem('img_id').children.item(0);

    const next_btn = document.getElementById('next_btn');
    const prev_btn = document.getElementById('prev_btn');


    const thumbBlocks = document.querySelectorAll('.thumb__block');
    const firstThumbBlockContent = thumbBlocks[0];
    const thumbnail = firstThumbBlockContent.getElementsByTagName('img')[0]
    const descriptions = firstThumbBlockContent.getElementsByTagName('span');

    const title = descriptions[0];
    const desc = descriptions[1];
    const date = descriptions[2];
    const urls = descriptions[3];
    const img_id = descriptions[4];
    let current_img_idx = 0;


// mainImage.src = getImgPath(thumbnail.src);
// mainImage.alt = thumbnail.alt;


    mainImage_title.textContent = title.textContent;
    mainImage_desc.textContent = desc.textContent;
    mainImage_date.textContent = get_date(date.textContent);
    mainImage_urls.textContent = urls.textContent;

    mainImage_id.textContent = img_id.textContent;


    next_btn.addEventListener('click', (event) => {
        current_img_idx++;
        if (current_img_idx >= thumbBlocks.length) {
            current_img_idx = thumbBlocks.length - 1;
        }
        let thumbBlock = thumbBlocks[current_img_idx];
        set_main_img(thumbBlock, current_img_idx);
        mainView.style.display = 'flex';
    });

    prev_btn.addEventListener('click', (event) => {
        current_img_idx--;
        if (current_img_idx < 0) {
            current_img_idx = 0;
        }
        let thumbBlock = thumbBlocks[current_img_idx];
        set_main_img(thumbBlock, current_img_idx);
        mainView.style.display = 'flex';

    });

    mainView.addEventListener('click', (event) => {
        console.log(event.target.tagName)
        //   if (event.target.id === "next_btn"||event.target.id === "prev_btn") {
        //   return;
        // }
        if (event.target.tagName === "BUTTON") {
            return;
        }
        mainView.style.display = 'none';
    });


    thumbnail.classList.toggle('active');
    let old_active = thumbnail;
    thumbBlocks.forEach(function (thumbBlock, index) {
        thumbBlock.addEventListener('click', (event) => {
            set_main_img(thumbBlock, index);
        });
    });


    function set_main_img(thumbBlock, index) {

        let target = thumbBlock.getElementsByClassName('thumb__img')[0];
        target.classList.toggle('active');
        old_active.classList.toggle('active');
        old_active = target;

        mainView.style.display = 'flex';
        const image = thumbBlock.getElementsByTagName('img')[0];
        const descriptions = thumbBlock.getElementsByTagName('span');
        const title = descriptions[0];
        const desc = descriptions[1];
        const date = descriptions[2];
        const urls = descriptions[3];
        const img_id = descriptions[4];
        // mainImage.src = getImgPath(image.src);
        // mainImage.alt = image.alt;

        mainView.style.backgroundImage = `url(${getImgPath(image.src)})`;


        mainImage_title.textContent = title.textContent;
        mainImage_desc.textContent = desc.textContent;
        mainImage_date.textContent = get_date(date.textContent);
        mainImage_urls.textContent = urls.textContent;
        mainImage_id.textContent = img_id.textContent;
        current_img_idx = index;
    }

}
/**Блок добавления новой картинки*/
const imgEditMode = document.getElementById('edit_mode');
const newImgForm = document.getElementById('new_img_form');
const textFields = newImgForm.getElementsByClassName('txt-input');
const idField = textFields.namedItem('id');
const imageField = document.getElementById('img_file');
const titleField = textFields.namedItem('title');
const descField = textFields.namedItem('desc');
const dateField = textFields.namedItem('date');
const urlsField = textFields.namedItem('url');

const submitBtn = document.getElementById("submitButton");

let header = document.getElementById('portfolio_buttons');
const button = document.createElement('button');
button.innerHTML = 'Добавить';
header.appendChild(button);
button.addEventListener("click", () => {
    imgEditMode.value = "new_image";
    imgEditMode.required = true;
    imageField.required = true;
    titleField.required = true;
    idField.required = false;
    descField.required = false;
    dateField.required = false;
    urlsField.required = false;

    imageField.value = "";
    titleField.value = "";
    descField.value = "";
    dateField.value = "";
    urlsField.value = "";
    idField.value = "";
    if (newImgForm.style.display === 'none') {
        newImgForm.style.display = 'flex';
        newImgForm.style.zIndex = 'var(--max-z-index)';
        submitBtn.innerHTML = "Отправить"
    } else {
        newImgForm.style.display = 'none';
        newImgForm.style.zIndex = '-1';
    }
});

/**Блок редактирования картинки*/
    // const editImgForm = document.getElementById('new_img_form');
    // let header = document.getElementsByClassName('header-right')[0];
let editbutton = document.createElement('button');

editbutton.innerHTML = 'Редактировать';
header.appendChild(editbutton);
editbutton.addEventListener("click", () => {
    imgEditMode.value = "edit_image";
    imageField.required = false;
    titleField.required = true;
    idField.required = true;
    descField.required = false;
    dateField.required = false;
    urlsField.required = false;

    titleField.value = mainImage_title.textContent;
    descField.value = mainImage_desc.textContent;
    dateField.value = get_format_date(mainImage_date.textContent);
    urlsField.value = mainImage_urls.textContent;
    idField.value = mainImage_id.textContent;

    if (newImgForm.style.display === 'none') {
        newImgForm.style.display = 'flex';
        newImgForm.style.zIndex = 'var(--max-z-index)';
        submitBtn.innerHTML = "Сохранить"
    } else {
        newImgForm.style.display = 'none';
        newImgForm.style.zIndex = '-1';
    }

});

/**Блок удаления картинки*/
const deletebutton = document.createElement('button');

deletebutton.innerHTML = 'Удалить';
header.appendChild(deletebutton);
deletebutton.addEventListener("click", () => {
    imageField.required = false;
    titleField.required = false;
    idField.required = true;
    descField.required = false;
    dateField.required = false;
    urlsField.required = false;
    imgEditMode.value = "delete_image";
    submitBtn.innerHTML = "Удалить"
    idField.value = mainImage_id.textContent;
    submitBtn.click();
});
// submitBtn.ontouchend();
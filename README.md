<span style="color:red">
# pip freeze > requirements.txt
</span>

###### https://django.fun/ru/docs/django/4.1/ref/models/fields/
# MARCDOWN
# Для работы джанго требуется установить эти пакеты:	
1. _pip install Pillow_
2. _pip install django-admin_

### Далее требуется создать проект командой:
#### django-admin startproject *MySite* .
<span style="color:red">Обязательно через пробел поставить точку </span>.

# Наше приложение называется index

## Далее нужно создать приложение = страница сайта командой:

#### django-admin startapp *index*
#### в файле MySite/settings - прописать наше приложение в INSTALLED_APPS

#### в файле MySite/urls в urlpatterns прописоть роут до urls нашего приложения
<pre>
urlpatterns = [
    path('', include('index.urls')),
    или path('', index.urls', name = 'index_in_urls_for_using_in_html_for_activity'),
    или path('index/', index.urls', name = 'index_in_urls_for_using_in_html_for_activity'),
    path('admin/', admin.site.urls),#прописан по умолчанию
]
include позволяет подгружать страницу только при переходе на нее.
в случае использования include потребуется создать urls в index
и там прописать

urlpatterns = [
    path('', views.indexView, name='index_in_urls_for_using_in_html_for_activity'),
    path('int:article_id>/', views.detailView, name='detail_in_urls'),#Это пример работы с бд
]

Прямое прописывание путей - подгружает страницу сразу,
что приводит к увеличению скорости просмотра сайта и увеличению нагрузки на траффик и железо с обоих концов

параметр name - создает переменную, которую можно будет вставить в какую нибудь страницу
в кнопку/ссылку/активный элмемент, и при нажатии будет происходить переход на наше приложение
то есть эта переменная позволит избавиться от ручного прописывания адреса в адресной строке, и назначить это
действие активному эдементу
</pre>
## Для статических файлов в том же файле добавить:
> STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]

### А для хранения картинок добавить еще это:
> MEDIA_URL = 'media/'

> MEDIA_ROOT = os.path.join(BASE_DIR,'media')

### в файле index/views.py сделать метод:
<pre>
def inputsView(request):
    some_variable = "Привет мир"
    articles = Article.objects.all()
    article = get_object_or_404(Article, pk = article_id)
    from_request_var = request.GET.get('from_form_submit_var_in_name_attr')
    context_for_response = {'html_variable': some_variable,
                            'html_articles': articles,
                            'html_article': article,
                            'html_variable': some_variable,
                            'html_from_request_var': from_request_var,
                            }
    return render(request,template_name='index/index.html', context=context_for_response)
</pre>
###### Здесь видно, что нужно указать путь к нашей странице, а в контексте передать значения, которые будут считываться
###### и выводиться в html файле. Переменные могут быть созданы из запроса (context_for_response),
###### или базы данных (articles и article)

#### В html нужно прописать:
<pre>


!DOCTYPE html
{% load static %}
html lang="en"
head
    meta charset="UTF-8"
    titleindex/title
    link rel="stylesheet" href="{% static 'css/style.css' %}"
/head

в index/admin пишем:
admin.site.register(Article)

в index/models пишем:
<pre>

class Article(models.Model):
    title = models.CharField(max_length=15)  # Ограниченная строка
    desc= models.CharField(max_length=50)  # Ограниченная строка
    image= models.ImageField(upload_to='blog/image')  # строка по изображению (отдельный тип данных)
    date = models.DateField()  # Дата
    url = models.URLField()  # Ссылка
    number = models.PositiveSmallIntegerField()
    f1 = models.JSONField()

Это пример создания базы данных. название класса должно быть в тему. Здесь название взято из примера
Все переменные - это поля таблицы. В общем то тут она и строится
</pre>

Вот так можно будет попасть на наше приложение из другой  страницы:
a href="{% url 'from_form_submit_var_in_name_attr' %}" class="link" Переход на наше приложение /a
Вот так можно задать переменную для передачи занчения поля в someView
input type="text" name="from_form_submit_var_in_name_attr"
</pre>


#### py manage.py migrate
#### py manage.py makemigrations  
#### py manage.py migrate
<span style="color:red">Создать суперпользователя получиться только после выполнения двух верхних команд </span>.
#### py manage.py createsuperuser  
там попросят указать почту логин и пароль админа - следовать инструкции<br>
<span style="color:red">Теперь мы можем залезть в /adnmin</span>.



### Так запускается сервер:
#### py manage.py runserver *8000*
## Пояснение
В задании требовалось использовать максимум полей таблицы,
Эта задача простая. Сложнее было добраться до самой таблицы, и желательно,
запомнить все действия.
На момент написания пояснения добавил в таблицу пару полей - с этим не возникло ни каких
проблем. По этому решил поля отложить, и по мере возможности, как то преобразовать
код, или добавить комментариев, что бы было отчетливо видно - какая переменная
куда ведет.




#### Пока искал стилизацию ридми - нашел анимацию. Пока слишком сложно для понимания так как ссылается на какой то ресурс
#### Получается без него работать не будет
# Ссылка
[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Computer+science+student)](https://git.io/typing-svg)
# Просто текст

![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Computer+science+student)
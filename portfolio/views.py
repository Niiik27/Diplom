from io import BytesIO

import PIL
from PIL import Image
from django.contrib.auth.models import User
from profile.models import CustomUser
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import OperationalError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
import APP_NAMES
from .forms import ArtworkForm

app_name = APP_NAMES.PORTFOLIO[APP_NAMES.NAME]
from .models import Artwork

verbose_name = APP_NAMES.PORTFOLIO[APP_NAMES.VERBOSE]


def get_date(date):
    day_list = ['первое', 'второе', 'третье', 'четвёртое',
                'пятое', 'шестое', 'седьмое', 'восьмое',
                'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
                'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
                'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
                'двадцать первое', 'двадцать второе', 'двадцать третье',
                'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
                'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
                'тридцатое', 'тридцать первое']
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    newdate = date[:date.rindex(' ')]
    year = int(newdate[newdate.rindex(' '):len(newdate)])
    newdate = date[:newdate.rindex(' ')]
    month_str = str(newdate[newdate.rindex(' '):len(newdate)]).strip(' ')
    day_str = date[:newdate.rindex(' ')].strip(' ')

    day = str(day_list.index(day_str) + 1).rjust(2, '0')
    month = str(month_list.index(month_str) + 1).rjust(2, '0')

    return f'{year}-{month}-{day}'


def make_thumb(original_image, max_size=(300, 300)):
    # Открываем оригинальное изображение с помощью Pillow
    img = Image.open(original_image)
    # Уменьшаем изображение до заданных размеров (если оно больше)
    img.thumbnail(max_size)
    # Создаем байтовый поток для сохранения изображения
    image_stream = BytesIO()
    img.save(image_stream, format='JPEG')  # Вы можете выбрать другой формат, если это не JPEG

    # Создаем объект InMemoryUploadedFile для уменьшенного изображения
    resized_image = InMemoryUploadedFile(
        image_stream,
        None,
        original_image.name,  # Имя файла остается тем же, что и у оригинала
        'image/jpeg',
        image_stream.tell(),
        None
    )

    return resized_image


# def get_Full_Image(request, img_id):
#     portfolio = Artwork.objects.filter(user=request.user, id=img_id)
#     return render(request, template_name=f'./{app_name}/{app_name}.html',
#                   context={'form': form, 'portfolio': portfolio, 'page_name': verbose_name, 'page_style': app_name})
#
# return redirect(APP_NAMES.PORTFOLIO)

def portfolioView(request, username):
    # print(request)
    # print(type(request))
    # print(dir(request))
    # print(request.user.id)
    # print(dir(request.user))  # Откуда же здесь берется юзер?
    # print(request.method)
    if request.method == 'GET':
        # print('****portfolio****', 'portfolio')
        # print('****portfolio****', request.user.username)

        try:
            user = CustomUser.objects.get(username=username)
            portfolio = Artwork.objects.filter(user=user)
            print(portfolio)

            # portfolio = get_object_or_404(Artwork, username=username)

            # portfolio = get_object_or_404(Artwork, username=request.user.username)
            # print(dir(portfolio.image))
            # print(portfolio.image.path)
        except Http404 as e:
            # print(str(e))
            portfolio = None
            # print('****portfolio****',portfolio)
            # print(dir(portfolio.image))
        except OperationalError as e:
            # print(str(e))
            portfolio = None
        form = ArtworkForm()

        return render(request, template_name=f'./{app_name}/{app_name}.html',
                      context={'form': form, 'username': username, 'portfolio': portfolio, 'page_name': verbose_name,
                               'page_style': app_name})

    else:
        # print('****portfolio****', 'portfolio')
        # print('****portfolio****', 'portfolio')
        # print('****portfolio****', 'portfolio')
        # print('****portfolio****', 'portfolio')
        # print('****portfolio****', 'portfolio')
        print(str(request.POST))

        edit_mode = request.POST['edit_mode']
        # edit_mode = request.POST['edit_btn']
        portfolio: Artwork = Artwork(user=request.user)
        match edit_mode:
            case 'new_image':
                new_img = request.FILES.get('image')
                new_title = request.POST.get('title')
                new_desc = request.POST.get('desc')
                new_date = request.POST.get('date')
                new_url = request.POST.get('url')
                if new_img:
                    portfolio.image = new_img
                    portfolio.thumb = make_thumb(new_img)
                else:
                    return redirect(APP_NAMES.PORTFOLIO[APP_NAMES.NAME], request.user)
                if new_title:
                    portfolio.title = new_title
                else:
                    return redirect(APP_NAMES.PORTFOLIO[APP_NAMES.NAME], request.user)
                if new_desc:
                    portfolio.desc = new_desc
                if new_date:
                    portfolio.date = new_date
                if new_url:
                    portfolio.url = new_url
                portfolio.save()

                # form = ArtworkForm(request.POST, request.FILES)
                # if form.is_valid():
                #     print('saved ' * 100)
                #     original_image = form.cleaned_data['image']
                #     artwork = form.save(commit=False)
                #     artwork.user = request.user
                #     artwork.image = original_image
                #     artwork.thumb = make_thumb(original_image)
                #     artwork.save()

                return redirect(APP_NAMES.PORTFOLIO[APP_NAMES.NAME], request.user.username)
            case 'edit_image':
                portfolio: Artwork = Artwork.objects.get(user=request.user, id=request.POST['id'])
                edit_img = request.FILES.get('image')
                edit_title = request.POST.get('title')
                edit_desc = request.POST.get('desc')
                edit_date = request.POST.get('date')
                edit_url = request.POST.get('url')
                if edit_img:
                    portfolio.image = edit_img
                    portfolio.thumb = make_thumb(edit_img)
                if edit_title:
                    portfolio.title = edit_title
                # if edit_desc:
                portfolio.desc = edit_desc
                # if edit_date:
                portfolio.date = edit_date
                # if edit_url:
                portfolio.url = edit_url
                portfolio.save()

                return redirect(APP_NAMES.PORTFOLIO[APP_NAMES.NAME], request.user.username)
            case 'delete_image':
                portfolio: Artwork = Artwork.objects.get(user=request.user, id=request.POST['id'])
                portfolio.delete()
                return redirect(APP_NAMES.PORTFOLIO[APP_NAMES.NAME], request.user.username)
            case _:
                print('error')
                return redirect(APP_NAMES.PORTFOLIO[APP_NAMES.NAME], request.user.username)

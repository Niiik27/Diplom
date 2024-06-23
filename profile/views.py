import json
from io import BytesIO
from PIL import Image
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView, DetailView, View
import requests
from django.core.files.base import ContentFile
from Print import Print
from _Brigada73.socket_client import SOCKET
from orders.models import Order
from teams.models import Team
from .forms import *
from .models import CustomUser

app_name = APP_NAMES.PROFILE[APP_NAMES.NAME]
verbose_name = APP_NAMES.PROFILE[APP_NAMES.VERBOSE]


def take_image_from_url(url):
    photo_url = url[0]
    if photo_url:
        response = requests.get(photo_url)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = Image.open(img_data)

            new_size = (300, 300)
            img.thumbnail(new_size)

            pathURL = photo_url.split("?")[0]
            imgExt = pathURL[pathURL.rfind('.') + 1:len(pathURL)]
            if imgExt.lower() == 'jpg':
                imgExt = 'jpeg'
            filename = pathURL.split('/')[-1]

            # Преобразуем изображение в байты
            buffer = BytesIO()
            img.save(buffer, format=imgExt)
            image_file = ContentFile(buffer.getvalue(), name=filename)

            # Сохраняем изображение в поле ImageField
            # self.image.save(filename, image_file)
            return image_file
        return None
    return None


def is_social_profile(link, social_id):
    start_link = 'https://'
    if link.startswith(start_link):
        dot_pos = link.index('.')
        base_link = link[len(start_link):]
        base_name = link[len(start_link):dot_pos]
        dot_pos = base_link.index('.') + 1
        domain = base_link[dot_pos:base_link.index('/')]

        social = SocialList.objects.get(pk=social_id)
        social_dict = json.loads(social.template_string)
        return base_name in social_dict['domain_names'] and domain in social_dict['domains']

        # return(base_name==templates[0] and domain==templates[1])


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser

    template_name = f'{APP_NAMES.VIEW[APP_NAMES.NAME]}/regular.html'
    context_object_name = 'profile_user'
    slug_field = 'username'  # Поле, используемое для идентификации пользователя в URL
    slug_url_kwarg = 'username'  # Параметр в URL, содержащий имя пользователя

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        profile_user = context['object']
        if profile_user.status:
            match profile_user.status.name:
                case 'Заказ':
                    return self.customer_profile(context)
                case 'Прораб':
                    return self.brigadir_profile(context)
                case 'Мастер':
                    return self.master_profile(context)
                case _:
                    return self.regular_profile(context)
        else:
            return self.regular_profile(context)

    def customer_profile(self, context):
        user = self.request.user
        profile_user = context['object']
        self.template_name = f'{APP_NAMES.VIEW[APP_NAMES.NAME]}/customer.html'
        order = Order.objects.get(customer=profile_user)
        if order is not None:
            context['order_master'] = order.master
        context['page_style'] = APP_NAMES.VIEW[APP_NAMES.NAME]
        context['username'] = user.username
        return context

    def brigadir_profile(self, context):
        user = self.request.user
        profile_user = context['object']
        user_social_profiles = UserSocial.objects.filter(user=profile_user)
        social_list = SocialList.objects.all()
        self.template_name = f'{APP_NAMES.VIEW[APP_NAMES.NAME]}/brigadir.html'

        sl_res = {}
        for i in range(len(social_list)):
            social_name = social_list[i].name
            social_ico = social_list[i].icon_path
            for j in range(len(user_social_profiles)):
                profile = user_social_profiles[j]
                if len(profile.link) > 0:
                    if profile.social_id == i + 1:
                        sl_res[social_name] = social_ico, profile.link
                        break
        context['social_list'] = sl_res
        try:
            order = Order.objects.get(master=profile_user)
        except Order.DoesNotExist:
            order = None
        if order is not None:
            context['order_customer'] = order.customer
        teams = Team.objects.filter(brigadir=user)
        context['teams'] = teams
        context['page_style'] = APP_NAMES.VIEW[APP_NAMES.NAME]
        context['username'] = user.username
        return context

    def master_profile(self, context):
        user = self.request.user
        profile_user = context['object']
        user_social_profiles = UserSocial.objects.filter(user=profile_user)
        social_list = SocialList.objects.all()
        self.template_name = f'{APP_NAMES.VIEW[APP_NAMES.NAME]}/master.html'

        sl_res = {}
        for i in range(len(social_list)):
            social_name = social_list[i].name
            social_ico = social_list[i].icon_path
            for j in range(len(user_social_profiles)):
                profile = user_social_profiles[j]
                if len(profile.link) > 0:
                    if profile.social_id == i + 1:
                        sl_res[social_name] = social_ico, profile.link
                        break
        context['social_list'] = sl_res
        try:
            order = Order.objects.get(master=profile_user)
        except Order.DoesNotExist:
            order = None
        if order is not None:
            context['order_customer'] = order.customer
        teams = Team.objects.filter(brigadir=user)
        context['teams'] = teams
        context['page_style'] = APP_NAMES.VIEW[APP_NAMES.NAME]
        context['username'] = user.username
        return context

    def regular_profile(self, context):
        user = self.request.user
        profile_user = context['object']
        user_social_profiles = UserSocial.objects.filter(user=profile_user)
        social_list = SocialList.objects.all()
        self.template_name = f'{APP_NAMES.VIEW[APP_NAMES.NAME]}/regular.html'

        sl_res = {}
        for i in range(len(social_list)):
            social_name = social_list[i].name
            social_ico = social_list[i].icon_path
            for j in range(len(user_social_profiles)):
                profile = user_social_profiles[j]
                if len(profile.link) > 0:
                    if profile.social_id == i + 1:
                        sl_res[social_name] = social_ico, profile.link
                        break
        context['social_list'] = sl_res
        try:
            order = Order.objects.get(master=profile_user)
        except Order.DoesNotExist:
            order = None
        if order is not None:
            context['order_customer'] = order.customer
        teams = Team.objects.filter(brigadir=user)
        context['teams'] = teams
        context['page_style'] = APP_NAMES.VIEW[APP_NAMES.NAME]
        context['username'] = user.username
        return context


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = f'{APP_NAMES.LOGIN[APP_NAMES.NAME]}/index.html'
    redirect_authenticated_user = True

    # success_url = reverse_lazy(APP_NAMES.HOME[APP_NAMES.NAME])
    def get_success_url(self):
        return f"/{APP_NAMES.PROFILE[APP_NAMES.NAME]}/{self.request.user.username}/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.LOGIN[APP_NAMES.NAME]
        return context


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = f'{APP_NAMES.REGISTER[APP_NAMES.NAME]}/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.get_form()
        context['page_style'] = APP_NAMES.REGISTER[APP_NAMES.NAME]

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=new_user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                if user.status is not None:
                    if user.status.name == 'Заказ':
                        Order.objects.create(customer=user)

                return redirect(reverse(f'{APP_NAMES.EDIT[APP_NAMES.NAME]}', kwargs={'username': user.username}))
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = EditUserForm
    template_name = f'{APP_NAMES.EDIT[APP_NAMES.NAME]}/regular.html'

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        user = get_object_or_404(CustomUser, pk=user_id)
        if user.status:
            match user.status.name:
                case 'Заказ':
                    return self.get_customer_form(self, request, *args, **kwargs)

                case 'Прораб':
                    return self.get_regular_form(self, request, *args, **kwargs)

                case _:
                    return self.get_regular_form(self, request, *args, **kwargs)
        else:
            return self.get_regular_form(self, request, *args, **kwargs)

    def get_customer_form(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        user = get_object_or_404(CustomUser, pk=user_id)
        form = EditCustomerForm(instance=user)
        context = {'form': form}
        self.template_name = f'{APP_NAMES.EDIT[APP_NAMES.NAME]}/customer.html'
        form.fields.pop('password1')
        form.fields.pop('password2')
        context['address_form'] = AddressForm(instance=user.address)
        context['fine_form'] = FineForm()
        context['contacts_form'] = ContactsForm(instance=user.user_contacts)
        context['page_style'] = APP_NAMES.EDIT[APP_NAMES.NAME]
        return self.render_to_response(context)

    def get_regular_form(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        user = get_object_or_404(CustomUser, pk=user_id)
        print(user.status)

        form = EditUserForm(instance=user)
        context = {'form': form}
        self.template_name = f'{APP_NAMES.EDIT[APP_NAMES.NAME]}/regular.html'

        form.fields.pop('password1')
        form.fields.pop('password2')
        # print('context', context)

        context['address_form'] = AddressForm(instance=user.address)
        user_social_profiles = UserSocial.objects.filter(user=user)
        social_list = SocialList.objects.all()
        sl_res = {}
        for i in range(len(social_list)):
            social_name = social_list[i].name
            social_ico = social_list[i].icon_path
            sl_res[social_name] = social_ico, ""
            for j in range(len(user_social_profiles)):
                profile = user_social_profiles[j]
                if len(profile.link) > 0:
                    if profile.social_id == i + 1:
                        sl_res[social_name] = social_ico, profile.link
                        break
        context['social_list'] = sl_res
        context['fine_form'] = FineForm()
        context['contacts_form'] = ContactsForm(instance=user.user_contacts)
        context['page_style'] = APP_NAMES.EDIT[APP_NAMES.NAME]

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        user = self.request.user
        # user_id = user.pk
        # user = get_object_or_404(CustomUser, pk=user_id)
        # if request.POST:
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # if password1 == password2:
        photo_url = (request.POST['photo_url']),
        image = None
        if photo_url:
            image = take_image_from_url(photo_url)
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST.get('last_name')
        email = request.POST['email']
        birth = request.POST['birth']
        about = request.POST['about']
        specialisation = request.POST.getlist('specialisation')
        status = request.POST.get('status')
        qualify = request.POST['qualify']
        social_link = request.POST.getlist('social_link')
        social_indexes = [index + 1 for index, link in enumerate(social_link) if link]
        allow = request.POST.getlist('allow')
        city = request.POST['city']
        district = request.POST['district']
        street = request.POST['street']
        house_number = request.POST['house_number']
        apartment = request.POST['apartment']
        postal_code = request.POST['postal_code']
        phone = request.POST['phone']
        messengers = request.POST.getlist('messenger')

        user.username = username
        user.photo_url = photo_url[0]
        user.image = image
        user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.email = email
        if birth:
            user.birth = birth
        if status:
            status_obj = Status.objects.get(id=status)
            user.status = status_obj
        user.about = about
        try:
            qualify_obj = Qualify.objects.get(id=qualify)
            user.qualify = qualify_obj

        except ValueError:
            qualify_obj = 0
        user.specialisation.clear()
        user.specialisation.add(*specialisation)
        user.allow.clear()
        user.allow.add(*allow)
        user.social_list.clear()
        user.social_list.add(*social_indexes)
        user.save()

        if user.status.name == 'Заказ':
            order, created = Order.objects.get_or_create(customer=user)
            ws = SOCKET("ws://127.0.0.1:8002/ws/notify/", request)
            ws.connect()
            ws.send_notify("", "from_server_notify_new_order")

        contact_user = Contacts.objects.get(user=user)
        contact_user.phone = phone
        contact_user.save()
        # contact_user.messenger.add(*messengers)
        selected_messengers = MessengerList.objects.filter(id__in=messengers)
        contact_user.messenger.set(selected_messengers)

        for i in range(len(social_link)):
            link = social_link[i]
            if link:
                if is_social_profile(link, i + 1):
                    try:
                        user_social = UserSocial.objects.get(user=user, social_id=i + 1)
                        user_social.link = link
                        user_social.save()
                    except UserSocial.DoesNotExist:
                        UserSocial.objects.create(user=user, link=link, social_id=i + 1)
            else:
                try:
                    user_social = UserSocial.objects.get(user=user, social_id=i + 1)
                    user_social.delete()
                except UserSocial.DoesNotExist:
                    pass

        address_user = Address.objects.get(user=user)
        if city:
            city_obj = City.objects.get(id=city)
            address_user.city = city_obj
        address_user.district = district
        address_user.street = street
        address_user.house_number = house_number
        if apartment:
            address_user.apartment = apartment
        if postal_code:
            address_user.postal_code = postal_code
        address_user.save()

        return redirect(self.get_success_url())

        # else:
        #     return redirect(request.get_full_path())

    def get_success_url(self):
        return reverse_lazy(APP_NAMES.PROFILE[APP_NAMES.NAME], kwargs={'username': self.request.user.username})

    def get_total_orders(self, me):
        new_orders = Order.objects.filter(confirmed=False)
        customer_ids = []
        for order in new_orders:
            customer = order.customer
            if customer.address.city == me.address.city:
                customer_ids.append(customer)
        num_orders = len(customer_ids)
        return num_orders


class CustomUserListView(ListView):
    model = CustomUser
    template_name = f'{APP_NAMES.USERS[APP_NAMES.NAME]}/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.status.name == 'Заказ':  # Нужно для ... возможно уже не нужно
            order = Order.objects.get(customer=self.request.user)
            if order is not None:
                context['order_master'] = order.master
        context['page_style'] = APP_NAMES.USERS[APP_NAMES.NAME]
        return context


class CustomUserListEdit(LoginRequiredMixin, TemplateView):  # (ListView):#
    model = CustomUser
    template_name = f'{APP_NAMES.USERS[APP_NAMES.NAME]}/edit_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.status.name == 'Заказ':
            order = Order.objects.get(customer=self.request.user)
            if order is not None:
                context['order_master'] = order.master
        users = CustomUser.objects.all()
        # context = {'users': []}
        context['customuser_list'] = {}

        for user in users:
            user_data = {}
            context['customuser_list'][user.id] = user_data
            user_data['image'] = user.image
            user_data['photo_url'] = user.photo_url

            user_data['login'] = user.username

            address_res = {}
            city_list = City.objects.all()
            ci_res = {}
            for i in range(city_list.count()):
                city_item = city_list[i]
                ci_res[city_item.name] = city_item == user.address.city
            address_res['city'] = ci_res

            # address_res['Город'] =  user.address.city.name
            address_res['Район'] = user.address.district
            address_res['Улица'] = user.address.street
            address_res['Номер дома'] = user.address.house_number
            address_res['Квартира'] = user.address.apartment
            address_res['Индекс'] = user.address.postal_code

            user_data['address_list'] = address_res

            status_list = Status.objects.all()
            stat_res = {}
            for i in range(status_list.count()):
                status_item = status_list[i]
                stat_res[status_item.name] = status_item == user.status
            user_data['status_list'] = stat_res

            user_social_profiles = UserSocial.objects.filter(user=user)
            social_list = SocialList.objects.all()
            sl_res = {}

            for i in range(len(social_list)):
                social_name = social_list[i].name
                social_ico = social_list[i].icon_path
                sl_res[social_name] = social_ico, ""
                for j in range(len(user_social_profiles)):
                    profile = user_social_profiles[j]
                    if len(profile.link) > 0:
                        if profile.social_id == i + 1:
                            sl_res[social_name] = social_ico, profile.link
                            break
            user_data['social_list'] = sl_res

            contacts = Contacts.objects.get(user=user)
            user_data['phone_number'] = contacts.phone
            messenger_list = MessengerList.objects.all()
            mes_res = {}
            for messenger in messenger_list:
                messenger_name = messenger.name
                messenger_ico = messenger.icon_path
                mes_res[messenger.id] = [messenger_name, messenger_ico, messenger in contacts.messenger.all()]

            user_data['messenger_list'] = mes_res

            spec_list = Specialisations.objects.all()
            sp_res = {}
            for spec in spec_list:
                sp_res[spec.id] = [spec.specialisation, spec in user.specialisation.all()]

            user_data['spec_list'] = sp_res

            allow_list = Allowance.objects.all()
            al_res = {}
            for allow in allow_list:
                al_res[allow.id] = [allow.allow, allow in user.allow.all()]

            user_data['allow_list'] = al_res

        context['page_style'] = APP_NAMES.USERS[APP_NAMES.NAME]
        return context


@csrf_exempt
def save_user(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(CustomUser, pk=user_id)
            photo_url = data['photo_url'],
            image = None

            {'csrfmiddlewaretoken': ['LDHQewS5Raqd6ZN7r42kr4qNDvFVUIKynl5SqU25ANFWbr0Yid8iKM2wkEqE2InN'],
             'username': ['django'], 'photo_url': [
                'https://sun9-44.userapi.com/impf/7XxHnsMPsNDK6Br7u655OpyRoFcs-seeTSK55w/-xTYPRrNFSs.jpg?size=541x373&quality=96&sign=f2e0a9eff211bbdbda93a3694e7166df&type=album'],
             'first_name': ['Николай'], 'last_name': ['Меньшиков'], 'email': ['admin@example.com'],
             'birth': ['1980-10-27'], 'specialisation': ['1', '2', '4', '5', '6'], 'allow': ['1', '2'], 'status': ['1'],
             'qualify': ['3'], 'about': [
                'Учитывая ключевые сценарии поведения, начало повседневной работы по формированию позиции требует от нас анализа прогресса профессионального сообщества. Являясь всего лишь частью общей картины, многие известные личности своевременно верифицированы. Предварительные выводы неутешительны: базовый вектор развития обеспечивает широкому кругу (специалистов) участие в формировании глубокомысленных рассуждений.'],
             'social_link': ['', 'https://github.com/Niiik27/Diplom.git', '', '', '', '', 'https://badoo.com/feed',
                             'https://vk.com/feed', '', 'https://inst.com/feed', 'https://ok.ru/feed'],
             'phone': ['+75559863165'], 'messenger': ['2', '3', '4', '5'], 'city': ['1'], 'district': [''],
             'street': ['Островского'], 'house_number': ['58'], 'apartment': ['131'], 'postal_code': ['432071']}

            if photo_url:
                image = take_image_from_url(photo_url)
            username = data['login']
            # first_name = data['first_name']
            # last_name = data.get('last_name')
            # email = data['email']
            # birth = data['birth']
            # about = data['about']
            specialisation = data.get('specializations')

            status = data.get('status')
            # qualify = data['qualify']

            allow = data.get('permissions')

            address = data['address']
            city = int(address['city'])+1
            district = address['Район']
            street = address['Улица']
            house_number = address['Номер дома']
            apartment = address['Квартира']
            postal_code = address['Индекс']

            phone = data['phone_number']
            messengers = data.get('messengers')

            user.username = username
            user.photo_url = photo_url[0]
            user.image = image
            # user.first_name = first_name
            # if last_name:
            #     user.last_name = last_name
            # user.email = email
            # if birth:
            #     user.birth = birth
            if status:
                status_obj = Status.objects.get(id=status)
                user.status = status_obj
            # user.about = about
            # try:
            #     qualify_obj = Qualify.objects.get(id=qualify)
            #     user.qualify = qualify_obj
            #
            # except ValueError:
            #     qualify_obj = 0
            user.specialisation.clear()
            user.specialisation.add(*specialisation)
            user.allow.clear()
            user.allow.add(*allow)

            # social_list = [name for name in SocialList.objects.all(verbose_name)]
            social_list = SocialList.objects.values_list('name', flat=True)

            dict_socialLinks = data.get('dict_socialLinks')
            social_links_list = data.get('social_links_list')
            social_indexes = [index + 1 for index, link in enumerate(social_links_list) if link]
            user.social_list.clear()
            user.social_list.add(*social_indexes)
            user.save()

            # if user.status.name == 'Заказ':
            #     order, created = Order.objects.get_or_create(customer=user)
            #     ws = SOCKET("ws://127.0.0.1:8002/ws/notify/", request)
            #     ws.connect()
            #     ws.send_notify("", "from_server_notify_new_order")

            for i in range(len(social_list)):
                link = social_links_list[i]
                if link:
                    if is_social_profile(link, i + 1):
                        try:
                            user_social = UserSocial.objects.get(user=user, social_id=i + 1)
                            user_social.link = link
                            user_social.save()
                        except UserSocial.DoesNotExist:
                            UserSocial.objects.create(user=user, link=link, social_id=i + 1)
                    else:
                        try:
                            user_social = UserSocial.objects.get(user=user, social_id=i + 1)
                            user_social.delete()
                        except UserSocial.DoesNotExist:
                            pass

            contact_user = Contacts.objects.get(user=user)
            contact_user.phone = phone
            contact_user.save()
            # contact_user.messenger.add(*messengers)
            selected_messengers = MessengerList.objects.filter(id__in=messengers)
            contact_user.messenger.set(selected_messengers)

            address_user = Address.objects.get(user=user)
            if city:
                city_obj = City.objects.get(id=city)
                address_user.city = city_obj
            address_user.district = district
            address_user.street = street
            address_user.house_number = house_number
            if apartment:
                address_user.apartment = apartment
            if postal_code:
                address_user.postal_code = postal_code
            address_user.save()

            # user.photo_url = data['photo_url']
            # user.login = data['login']
            # user.address = data['address']
            # user.phone_number = data['phone_number']
            # user.status = data['status']
            # user.specializations = data['specializations']
            # user.permissions = data['permissions']
            # user.social_links = {item['key']: item['value'] for item in data['social_links']}
            # user.messengers = data['messengers']
            # user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Неправильный метод запроса'})


class CustomUserListSave2(UpdateView):  # (ListView):#
    model = CustomUser
    template_name = f'{APP_NAMES.USERS[APP_NAMES.NAME]}/edit_users.html'

    def get_success_url(self):
        return reverse_lazy(APP_NAMES.PROFILE[APP_NAMES.NAME], kwargs={'username': self.request.user.username})

    def post(self, request, *args, **kwargs):
        print('Получил пост запрос на сохранение', request.POST)

        data = json.loads(request.body)
        print(data)

        # user.photo_url = data['photo_url']
        # user.login = data['login']
        # user.address = data['address']
        # user.phone_number = data['phone_number']
        # user.status = data['status']
        # user.specializations = data['specializations']
        # user.permissions = data['permissions']
        # user.social_links = {item['key']: item['value'] for item in data['social_links']}
        # user.messengers = data['messengers']

        # return redirect(self.get_success_url())

        return JsonResponse({'success': True})
        # else:
        #     return JsonResponse({'success': False, 'error': 'User ID is missing'}, status=400)

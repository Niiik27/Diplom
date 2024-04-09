import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView, DetailView

import APP_NAMES
from .forms import *
from .models import CustomUser

app_name = APP_NAMES.PROFILE[APP_NAMES.NAME]
verbose_name = APP_NAMES.PROFILE[APP_NAMES.VERBOSE]


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser

    template_name = f'{APP_NAMES.VIEW[APP_NAMES.NAME]}/index.html'
    context_object_name = 'profile_user'
    slug_field = 'username'  # Поле, используемое для идентификации пользователя в URL
    slug_url_kwarg = 'username'  # Параметр в URL, содержащий имя пользователя

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        user_social_profiles = UserSocial.objects.filter(user=self.request.user)
        social_list = SocialList.objects.all()
        print(context)
        if user.status_id != len(Status.objects.all()):
            context['role'] = 'builder'
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
        else:
            context['role'] = 'customer'




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
        context['page_style'] = APP_NAMES.VIEW[APP_NAMES.NAME]
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
                return redirect(reverse(f'{APP_NAMES.PROFILE[APP_NAMES.NAME]}', kwargs={'username': user.username}))

                # return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = EditUserForm
    template_name = f'{APP_NAMES.EDIT[APP_NAMES.NAME]}/index.html'

    # success_url = reverse_lazy(APP_NAMES.HOME[APP_NAMES.NAME])
    # success_url = reverse_lazy('profile', kwargs={'username': form_class.fields['username']})
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        user = get_object_or_404(CustomUser, pk=user_id)
        if user.status_id != len(Status.objects.all()):

            form = EditUserForm(instance=user)
            context = {'form': form}
            context['role'] = 'builder'
        else:
            form = EditCustomerForm(instance=user)
            context = {'form': form}
            context['role'] = 'customer'
        form.fields.pop('password1')
        form.fields.pop('password2')

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
        print("sl_res", social_list)
        context['social_list'] = sl_res
        context['fine_form'] = FineForm()
        context['status_form'] = StatusForm()
        context['portfolio_form'] = PortfolioForm()
        context['notifications_form'] = NotificationsForm()
        context['team_form'] = TeamForm()
        context['card_form'] = CardForm()
        context['contacts_form'] = ContactsForm(instance=user.user_contacts)
        context['page_style'] = APP_NAMES.EDIT[APP_NAMES.NAME]

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        user = get_object_or_404(CustomUser, pk=user_id)
        # if request.POST:
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # if password1 == password2:
        #     print(password1, password2)
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
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
        user.first_name = first_name
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
        user.specialisation.add(*specialisation)
        user.allow.add(*allow)
        user.social_list.add(*social_indexes)
        user.save()
        contact_user = Contacts.objects.get(user=user)
        contact_user.phone = phone
        contact_user.save()
        # contact_user.messenger.add(*messengers)
        selected_messengers = MessengerList.objects.filter(id__in=messengers)
        contact_user.messenger.set(selected_messengers)

        for i in range(len(social_link)):
            link = social_link[i]
            if link:
                if (self.is_social_profile(link, i + 1)):
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
        # print(type(self.form_class))
        # print(dir(self.form_class))
        # print(self.form_class.changed_data.get_context)
        # return redirect(self.success_url)
        # return redirect(
        #     reverse_lazy(APP_NAMES.HOME[APP_NAMES.NAME], kwargs={'username': self.request.user.username}))
        return redirect(self.get_success_url())

        # else:
        #     return redirect(request.get_full_path())

    def get_success_url(self):
        return reverse_lazy(APP_NAMES.PROFILE[APP_NAMES.NAME], kwargs={'username': self.request.user.username})

    def is_social_profile(self, link, social_id):

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


class CustomUserListView(ListView):
    model = CustomUser
    template_name = f'{APP_NAMES.USERS[APP_NAMES.NAME]}/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.USERS[APP_NAMES.NAME]
        return context

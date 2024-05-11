from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class CustomUserForm(UserCreationForm):
    is_customer = forms.BooleanField(label='Я заказчик', required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'is_customer', ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('is_customer', False):
            last_status = Status.objects.last()
            user.status = last_status
        if commit:
            user.save()
        return user


class EditUserForm(UserCreationForm):
    birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        help_text="Выберите дату рождения",
        required=False
    )
    status = forms.ModelChoiceField(queryset=Status.objects.exclude(name__in=['Заказ', 'Прораб']), label='Статус')
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth',
                  'specialisation', 'status', 'qualify', 'social_list', 'allow', 'about']

        widgets = {
            'social_list': forms.CheckboxSelectMultiple,
            'allow': forms.CheckboxSelectMultiple,
            'specialisation': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        if args:
            self.post = args[0]
            self.user = kwargs.get('instance')
            self.address_formset = AddressFormSet(*args, **kwargs)

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.post:
            return None
        # user = self.user

        # if user is None:
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            # user.save()
            # self.save_m2m()

            specialisation = self.post.getlist('specialisation')
            allow = self.post.getlist('allow')
            phone = self.post['phone']
            messenger = self.post.getlist('messenger')
            city = self.post['city']
            district = self.post['district']
            street = self.post['street']
            house_number = self.post['house_number']
            apartment = self.post['apartment']
            postal_code = self.post['postal_code']
            # user.specialisation.clear()
            # user.save()
            user.specialisation.add(*specialisation)
            # user.allow.clear()
            user.allow.add(*allow)
            # user.save()
            # self.save_m2m()


            social_link = self.post.getlist('social_link')
            # social_indexes = [index + 1 for index, link in enumerate(social_link) if link]
            social_indexes = []

            for i in range(1, len(social_link) + 1):
                # for link in social_link:
                link = social_link[i - 1]
                if link:
                    UserSocial.objects.create(user=user, link=link, social_id=i)
                    social_indexes.append(i)
            user.social_list.add(*social_indexes)

            contact_user = Contacts.objects.get(user=user)
            contact_user.phone = phone
            contact_user.save()
            contact_user.messenger.add(*messenger)

            address_user = Address.objects.get(user=user)

            city_obj = City.objects.get(id=city)
            address_user.city = city_obj
            address_user.district = district
            address_user.street = street
            address_user.house_number = house_number
            address_user.apartment = apartment
            address_user.postal_code = postal_code
            address_user.save()
        return user

    def is_valid(self):

        # print(self.errors.all())
        # super().is_valid()
        # self.errors
        return self.is_bound and not self.errors
        # return True


class EditCustomerForm(UserCreationForm):
    birth = forms.DateField(
        label="Примерная дата окончания строительства",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        help_text="Выберите дату",
        required=False
    )
    about = forms.CharField(label="О заказе", required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    # status = forms.ModelChoiceField(queryset=Status.objects.exclude(name__in=['Заказчик', 'Прораб']), label='Статус')

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth', 'qualify', 'about']

    def __init__(self, *args, **kwargs):
        if args:
            self.post = args[0]
            self.user = kwargs.get('instance')
            self.address_formset = AddressFormSet(*args, **kwargs)

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.post:
            return None
        # user = self.user

        # if user is None:
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()

            phone = self.post['phone']
            messenger = self.post.getlist('messenger')
            city = self.post['city']
            district = self.post['district']
            street = self.post['street']
            house_number = self.post['house_number']
            apartment = self.post['apartment']
            postal_code = self.post['postal_code']

            contact_user = Contacts.objects.get(user=user)
            contact_user.phone = phone
            contact_user.save()
            contact_user.messenger.add(*messenger)

            address_user = Address.objects.get(user=user)

            city_obj = City.objects.get(id=city)
            address_user.city = city_obj
            address_user.district = district
            address_user.street = street
            address_user.house_number = house_number
            address_user.apartment = apartment
            address_user.postal_code = postal_code
            address_user.save()
        return user

    def is_valid(self):

        # print(self.errors.all())
        # super().is_valid()
        # self.errors
        return self.is_bound and not self.errors
        # return True

class EditProrabForm(UserCreationForm):
    birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        help_text="Выберите дату рождения",
        required=False
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth',
                  'specialisation', 'qualify', 'social_list', 'allow', 'about']
        widgets = {
            'social_list': forms.CheckboxSelectMultiple,
            'allow': forms.CheckboxSelectMultiple,
            'specialisation': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        if args:
            self.post = args[0]
            self.user = kwargs.get('instance')
            self.address_formset = AddressFormSet(*args, **kwargs)

        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        if not self.post:
            return None
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            specialisation = self.post.getlist('specialisation')
            allow = self.post.getlist('allow')
            phone = self.post['phone']
            messenger = self.post.getlist('messenger')
            city = self.post['city']
            district = self.post['district']
            street = self.post['street']
            house_number = self.post['house_number']
            apartment = self.post['apartment']
            postal_code = self.post['postal_code']
            user.specialisation.add(*specialisation)
            user.allow.add(*allow)
            social_link = self.post.getlist('social_link')
            social_indexes = []
            for i in range(1, len(social_link) + 1):
                link = social_link[i - 1]
                if link:
                    UserSocial.objects.create(user=user, link=link, social_id=i)
                    social_indexes.append(i)
            user.social_list.add(*social_indexes)
            contact_user = Contacts.objects.get(user=user)
            contact_user.phone = phone
            contact_user.save()
            contact_user.messenger.add(*messenger)
            address_user = Address.objects.get(user=user)
            city_obj = City.objects.get(id=city)
            address_user.city = city_obj
            address_user.district = district
            address_user.street = street
            address_user.house_number = house_number
            address_user.apartment = apartment
            address_user.postal_code = postal_code
            address_user.save()
        return user

    def is_valid(self):
        return self.is_bound and not self.errors

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        exclude = ['name']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'district', 'street', 'house_number', 'apartment', 'postal_code']


class UserSocialForm(forms.ModelForm):
    class Meta:
        model = UserSocial
        fields = ['link']


class SocialListForm(forms.ModelForm):
    class Meta:
        model = SocialList
        fields = ['name']


class MessengerListForm(forms.ModelForm):
    class Meta:
        model = MessengerList
        fields = ['name']


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['phone', 'messenger']
        widgets = {
            'messenger': forms.CheckboxSelectMultiple(attrs={'class': 'messenger-checkbox'}),
        }

    # def get_messenger_label(self, messenger):
    #     return f'<img src="{messenger.icon_path}" alt="{messenger.name}" class="messenger-icon"> {messenger.name}'
    #
    # def as_messenger_checkbox(self):
    #     return self._html_output(
    #         normal_row='<li>%(label)s %(field)s %(help_text)s</li>',
    #         error_row='%s',
    #         row_ender='</li>',
    #         help_text_html='%s',
    #         errors_on_separate_row=True,
    #     )


# class SpecialisationsForm(forms.ModelForm):
#     class Meta:
#         model = Specialisations
#         fields = ['specialisation']


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['fine']


# class StatusForm(forms.ModelForm):
#     class Meta:
#         model = Status
#         fields = ['name']


    # def get_status_choices(self):
    #     excluded_statuses = ['Заказчик', 'Бригадир']
    #     statuses = Status.objects.exclude(name__in=excluded_statuses)
    #     return [(status.id, status.name) for status in statuses]



# class PortfolioForm(forms.ModelForm):
#     class Meta:
#         model = Portfolio
#         fields = ['portfolio']
#
#
# class NotificationsForm(forms.ModelForm):
#     class Meta:
#         model = Notifications
#         fields = ['notification', 'new']


# class TeamForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ['customer', 'qualify', 'coworkers']
#
#
# class CardForm(forms.ModelForm):
#     class Meta:
#         model = Card
#         fields = ['number', 'date', 'cvs']


AddressFormSet = forms.inlineformset_factory(CustomUser, Address, form=AddressForm, can_delete=True, extra=0)
UserSocialFormSet = forms.inlineformset_factory(CustomUser, UserSocial, form=UserSocialForm, can_delete=True, extra=0)
# SocialListFormSet = forms.inlineformset_factory(CustomUser, SocialList, form=SocialListForm, can_delete=True, extra=0)
# MessengerListFormSet = forms.inlineformset_factory(CustomUser, MessengerList, form=MessengerListForm, can_delete=True, extra=0)
# ContactsFormSet = forms.inlineformset_factory(CustomUser, Contacts, form=ContactsForm, can_delete=True, extra=0)
# Другие наборы форм


# Создаем формсет, который будет содержать обе формы
# CustomUserFormSet = forms.inlineformset_factory(CustomUser,
#                                                 Card,
#
#                                                 form=CardForm, can_delete=False, extra=1)
# CustomUserFormSet = forms.inlineformset_factory(CustomUser,
#                                                 Card,
#                                                 City,
#                                                 Address,
#                                                 UserSocial,
#                                                 SocialList,
#                                                 MessengerList,
#                                                 Contacts,
#                                                 Allowance,
#                                                 Skills,
#                                                 Specialisations,
#                                                 Fine,
#                                                 Status,
#                                                 Portfolio,
#                                                 Notifications,
#                                                 Team,
#                                                 form=CardForm, can_delete=False, extra=1)


# CustomUser,
# Card,
# City,
# Address,
# UserSocial,
# SocialList,
# MessengerList,
# Contacts,
# Allowance,
# Skills,
# Specialisations,
# Fine,
# Status,
# Portfolio,
# Notifications,
# Team,


# class CustomUserForm(UserCreationForm):
#     birth = forms.DateField(
#         label="Дата рождения",
#         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
#         help_text="Выберите дату рождения",
#         required=False
#     )
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth',
#                   'specialisation', 'status', 'qualify', 'social_list', 'allow', ]
#         widgets = {
#             'social_list': forms.CheckboxSelectMultiple,
#             'allow': forms.CheckboxSelectMultiple,
#             'specialisation': forms.CheckboxSelectMultiple,
#             # 'usersocial': forms.TextInput,
#             # 'social_list': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название соцсети'}),
#         }
#     def __init__(self, *args, **kwargs):
#
#         if args:
#             self.post = args[0]
#         else:
#             self.post = []
#         super().__init__(*args, **kwargs)
#     def save(self, commit=True):
#         if self.post:
#             password1 = self.post['password1']
#             password2 = self.post['password2']
#             if password1 == password2:
#                 username = self.post['username']
#                 first_name = self.post['first_name']
#                 last_name = self.post['last_name']
#                 email = self.post['email']
#                 birth = self.post['birth']
#                 specialisation = self.post.getlist('specialisation')
#                 status = self.post['status']
#                 qualify = self.post['qualify']
#                 social_link = self.post.getlist('social_link')
#                 social_indexes = [index + 1 for index, link in enumerate(social_link) if link]
#                 allow = self.post.getlist('allow')
#                 city = self.post['city']
#                 district = self.post['district']
#                 street = self.post['street']
#                 house_number = self.post['house_number']
#                 apartment = self.post['apartment']
#                 postal_code = self.post['postal_code']
#                 phone = self.post['phone']
#                 messenger = self.post.getlist('messenger')
#                 status_obj = Status.objects.get(id=status)
#                 qualify_obj = Qualify.objects.get(id=qualify)
#
#                 new_user = CustomUser.objects.create(
#                             password=password1,
#                             username=username,
#                             first_name=first_name,
#                             last_name=last_name,
#                             email=email,
#                             birth=birth,
#                             status=status_obj,
#                             qualify=qualify_obj,
#                         )
#
#                 new_user.specialisation.add(*specialisation)
#                 new_user.allow.add(*allow)
#                 new_user.social_list.add(*social_indexes)
#
#                 contact_user = Contacts.objects.get(user=new_user)
#                 contact_user.phone = phone
#                 contact_user.save()
#                 contact_user.messenger.add(*messenger)
#
#                 for link in social_link:
#                     if link:
#                         UserSocial.objects.create(user=new_user, link=link)
#
#                 address_user = Address.objects.get(user=new_user)
#                 city_obj = City.objects.get(id=city)
#                 address_user.city = city_obj
#                 address_user.district = district
#                 address_user.street = street
#                 address_user.house_number = house_number
#                 address_user.apartment = apartment
#                 address_user.postal_code = postal_code
#                 address_user.save()
#                 return new_user
#         else:
#             return None


# class AllowanceForm(forms.ModelForm):
#     class Meta:
#         model = Allowance
#         fields = ['allow']


# class SkillsForm(forms.ModelForm):
#     class Meta:
#         model = Skills
#         fields = ['skill']

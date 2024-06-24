import json
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, View, DetailView, TemplateView
from django.http import JsonResponse

import APP_NAMES
from Print import Print
from _Brigada73.socket_client import SOCKET
from orders.models import Order
from profile.models import Status, Qualify, City, Specialisations, Allowance
from .models import CustomUser, Team

app_name = APP_NAMES.ORDERS[APP_NAMES.NAME]
verbose_name = APP_NAMES.ORDERS[APP_NAMES.VERBOSE]

class CreateTeamView(LoginRequiredMixin, TemplateView):
    model = Team

    template_name = f'{APP_NAMES.TEAMS[APP_NAMES.NAME]}/create.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['page_style'] = APP_NAMES.TEAM_CREATE[APP_NAMES.NAME]

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        if user.status.name == 'Прораб':
            # context['username'] = user.username
            order = Order.objects.get(master=user)

            if order is not None:
                context['order_customer'] = order.customer
                team = self.model.objects.filter(brigadir=user)
                specialisation_list = Specialisations.objects.all()
                status_list = Status.objects.exclude(name__in=['Прораб', 'Заказ', 'Мастер'])
                qualify_list = Qualify.objects.all()
                allow_list = Allowance.objects.all()
                specialists = []
                if team.count():
                    for j in range(team.count()):
                        team_spec = team[j]
                        spec_res = {}
                        spec_data = {}
                        coworker = team_spec.coworker
                        spec_data['id'] = team_spec.id

                        if coworker is not None:
                            spec_data['spec_name'] = coworker.username
                        for i in range(specialisation_list.count()):
                            spec_item = specialisation_list[i]
                            spec_res[spec_item.specialisation] = spec_item == team_spec.specialisation
                        spec_data['specialisations'] = spec_res

                        stat_res = {}
                        for i in range(status_list.count()):
                            status_item = status_list[i]
                            stat_res[status_item.name] = status_item == team_spec.status
                        spec_data['statuses'] = stat_res

                        qualify_res = {}
                        for i in range(qualify_list.count()):
                            qualify_item = qualify_list[i]
                            qualify_res[qualify_item.name] = qualify_item == team_spec.qualify
                        spec_data['qalifyes'] = qualify_res
                        allow_res = {}
                        for i in range(allow_list.count()):
                            allow_item = allow_list[i]
                            spec_allow_ids = team_spec.allow.values_list('id', flat=True)
                            allow_res[allow_item.allow] = allow_item.id in spec_allow_ids
                        spec_data['allows'] = allow_res
                        specialists.append(spec_data)
                else:
                    spec_item = {}
                    spec_data = {'id': 'tpl'}
                    for spec in specialisation_list:
                        spec_item[spec.specialisation] = False
                    spec_data['specialisations'] = spec_item
                    spec_item = {}
                    for status_item in status_list:
                        spec_item[status_item.name] = False
                    spec_data['statuses'] = spec_item
                    spec_item = {}
                    for qualify_item in qualify_list:
                        spec_item[qualify_item.name] = False
                    spec_data['qalifyes'] = spec_item
                    spec_item = {}
                    for allow_item in allow_list:
                        spec_item[allow_item.allow] = False
                    spec_data['allows'] = spec_item
                    specialists.append(spec_data)
                context['specialists'] = specialists
                print("context".upper(),context)

        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        workers = json.loads(request.POST.get('workers'))
        brigadir = self.request.user
        if brigadir and brigadir.status.name == 'Прораб':
            Team.objects.filter(brigadir=brigadir).delete()

            # team, _ = Team.objects.get_or_create(brigadir=brigadir)

            for worker in workers:
                Print.purpur(worker)
                specialisation_id = worker['specialisation']
                status_id = worker['status']
                qualify_id = worker['qualify']
                city_id = brigadir.address.city.id
                allowances = worker['allowances']

                specialisation_obj = Specialisations.objects.get(id=specialisation_id)
                status_obj = Status.objects.get(id=status_id)
                qualify_obj = Qualify.objects.get(id=qualify_id)
                city_obj = City.objects.get(id=city_id)

                new_team = Team.objects.create(
                    brigadir=brigadir,
                    specialisation=specialisation_obj,
                    status=status_obj,
                    qualify=qualify_obj,
                    city=city_obj,
                )
                new_team.allow.add(*allowances)
                new_team.save()

                ws = SOCKET("ws://127.0.0.1:8002/ws/notify/", request)
                ws.connect()
                ws.send_notify("","from_server_notify_new_team")
        return JsonResponse({'success': True})
        # else:
        #     return JsonResponse({'success': False, 'error': 'User ID is missing'}, status=400)
        # return Response(status=status.HTTP_200_OK)  # Возвращаем успешный ответ

class JoinTeamView(LoginRequiredMixin, TemplateView):
    model = Team
    def post(self, request, *args, **kwargs):
        team_id = request.POST.get('team_id')
        if team_id:
            already_exists = Team.objects.filter(coworker=request.user)
            if already_exists.exists():
                team_instance = already_exists.first()
                if team_instance.coworker is not None:
                    team_instance.coworker = None
                    team_instance.save()

            team = self.model.objects.get(id=team_id)
            if team.coworker != request.user:
                team.coworker = request.user
                team.save()
            # Print.yellow(team.brigadir.username, team.coworker.username, team.city.name,team.qualify.name, team.specialisation.specialisation)

            if team.coworker is not None:
                ws = SOCKET("ws://127.0.0.1:8002/ws/notify/", request)
                ws.connect()
                ws.send_notify_dara(type = "from_server_notify_coworker_joined", message = "", user_id =self.request.user.id, team_id = team_id)
            # else:
            #     return JsonResponse({'success': False, 'error': 'Already in team'}, status=400)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'User ID is missing'}, status=400)


class TeamsView(ListView):
    model = Team
    template_name = f'{APP_NAMES.TEAMS[APP_NAMES.NAME]}/teams_list.html'
    context_object_name = APP_NAMES.TEAM_LIST[APP_NAMES.NAME]
    ordering = ['-timestamp']

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = Team.objects.filter(brigadir__address__city=user.address.city)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.TEAMS[APP_NAMES.NAME]
        context['team_list'] = self.filter_coworker_teams(self.request.user)
        print(context['team_list'])
        return context

    def filter_coworker_teams(self, user, qualify=True, status=True, spec=True, allow=True, address=True):
        team_model = self.model
        required_filter = Q(coworker=None)
        if address: required_filter &= Q(city=user.address.city)
        if qualify: required_filter &= Q(qualify=user.qualify)
        if status: required_filter &= Q(status=user.status)
        if spec:
            for specialization in user.specialisation.all():
                required_filter &= Q(specialisation=specialization)
        if allow:
            user_allow_ids = set(allow.id for allow in user.allow.all())
            if user_allow_ids:
                for team in team_model.objects.all():
                    team_allow_ids = set(allow.id for allow in team.allow.all())
                    if user_allow_ids.issuperset(team_allow_ids):
                        required_filter &= Q(allow__id__in=team_allow_ids)
                        break

        specialisations = team_model.objects.filter(required_filter)

        if specialisations.count() == 0:
            if qualify:
                return self.filter_coworker_teams(user, qualify=False)
            elif status:
                return self.filter_coworker_teams(user, qualify=False, status=False)
            elif allow:
                return self.filter_coworker_teams(user, qualify=False, status=False, allow=False)
            elif spec:
                return self.filter_coworker_teams(user, qualify=False, status=False, allow=False, spec=False)
            elif address:
                return self.filter_coworker_teams(user, qualify=False, status=False, allow=False, spec=False,
                                                  address=False)
        return specialisations


class TeamView(ListView):
    model = Team
    template_name = f'{APP_NAMES.TEAMS[APP_NAMES.NAME]}/team_view.html'
    context_object_name = APP_NAMES.TEAM_LIST[APP_NAMES.NAME]
    ordering = ['-timestamp']

    slug_field = 'username'  # Поле, используемое для идентификации пользователя в URL
    slug_url_kwarg = 'username'  # Параметр в URL, содержащий имя пользователя


    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = Team.objects.filter(brigadir__address__city=user.address.city)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        match(user.status.name ):
            case 'Заказ':
                return self.get_order_data(context)
            case 'Прораб':
                return self.get_brigadir_data(context)
            # case _:
            #     return self.get_brigadir_data(context)


        if user.status.name == 'Прораб':
            # team_set = context[APP_NAMES.TEAM_LIST[APP_NAMES.NAME]]
            team_set = Team.objects.filter(brigadir=user)
        else:
            brigadir = Team.objects.filter(coworker=user).first()
            if brigadir:
                team_set = Team.objects.filter(brigadir=brigadir.brigadir)
            else:
                team_set = None

        if team_set:
            brigadir = team_set.first().brigadir

            team = self.model.objects.filter(brigadir=brigadir)
            context['team'] = team
            context['brigadir'] = brigadir

            for specialisation in team:
                print(specialisation.specialisation, specialisation.brigadir)

        if self.request.user.status.name == 'Заказ':
            order = Order.objects.get(customer=self.request.user)
            if order is not None:
                context['order_master'] = order.master

        # if profile_user.status:
        #     if profile_user.status.name == 'Заказ':
        #         order = Order.objects.get(customer=profile_user)
        #         if order is not None:
        #             context['order_master'] = order.master
        #     if profile_user.status.name == 'Прораб':
        #         order = Order.objects.get(master=profile_user)
        #         if order is not None:
        #             context['order_customer'] = order.customer
        #         teams = Team.objects.filter(brigadir=user)
        #         context['teams'] = teams

        # specialisations = self.model.objects.filter(brigadir__username=context['brigadir'])
        context['page_style'] = APP_NAMES.TEAM_VIEW[APP_NAMES.NAME]
        Print.yellow("Вернулли запрос")
        return context

    def get_brigadir_data(self,context):
        user = self.request.user
        team_set = Team.objects.filter(brigadir=user)
        if team_set:
            brigadir = team_set.first().brigadir
            team = self.model.objects.filter(brigadir=brigadir)
            context['team'] = team
            context['brigadir'] = brigadir
            # for specialisation in team:
            #     print(specialisation.specialisation,specialisation.brigadir)
        context['page_style'] = APP_NAMES.TEAM_VIEW[APP_NAMES.NAME]
        return context

    def get_order_data(self,context):
        user = self.request.user
        order = Order.objects.get(customer=user)
        if order is not None:
            master = order.master
            context['order_master'] = master
            context['brigadir'] = master
            team_set = Team.objects.filter(brigadir=master)
            context['team'] = team_set
        context['page_style'] = APP_NAMES.TEAM_VIEW[APP_NAMES.NAME]
        return context

class TeamDeleteUser(LoginRequiredMixin, TemplateView):
    model = Team
    def post(self, request, *args, **kwargs):
        team_id = request.POST.get('team_id')
        if team_id:
            team = self.model.objects.get(id=team_id)
            team.delete()

            # if team.coworker is not None:
            #     ws = SOCKET("ws://127.0.0.1:8002/ws/notify/", request)
            #     ws.connect()
            #     ws.send_notify_dara(type = "from_server_notify_coworker_joined", message = "", user_id =self.request.user.id, team_id = team_id)
            #

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'User ID is missing'}, status=400)
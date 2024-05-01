import json

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
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
        context['page_style'] = APP_NAMES.TEAMS[APP_NAMES.NAME]

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Бригада",context)
        user = self.request.user
        context['user'] = user
        print(user.status)

        if user.status.name == 'Прораб':
            order = Order.objects.get(master=user)
            if order is not None:
                context['order_customer'] = order.customer
            statuses = Status.objects.exclude(name__in=['Прораб', 'Заказ', 'Мастер'])
            if statuses is not None:
                context['statuses'] = statuses
            specialisations = Specialisations.objects.all()
            if specialisations is not None:
                context['specialisations'] = specialisations
            qualifyes = Qualify.objects.all()
            if qualifyes is not None:
                context['qualifies'] = qualifyes
            cities = City.objects.all()
            if cities is not None:
                context['cities'] = cities
            allowances = Allowance.objects.all()
            if allowances is not None:
                context['allowances'] = allowances

        context['page_style'] = APP_NAMES.TEAMS[APP_NAMES.NAME]
        context['username'] = user.username
        return context

    def post(self, request, *args, **kwargs):
        workers = json.loads(request.POST.get('workers'))
        Print.green(workers)
        brigadir = self.request.user
        if brigadir and brigadir.status.name == 'Прораб':
            Team.objects.filter(brigadir=brigadir).delete()

            # team, _ = Team.objects.get_or_create(brigadir=brigadir)

            for worker in workers:
                Print.purpur(worker)
                specialisation_id = worker['specialisation']
                status_id = worker['status']
                qualify_id = worker['qualify']
                city_id = worker['city']
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



class TeamsView(ListView):
    model = Team
    template_name = f'{APP_NAMES.TEAMS[APP_NAMES.NAME]}/team_list.html'
    context_object_name = APP_NAMES.TEAM_LIST[APP_NAMES.NAME]
    ordering = ['-timestamp']

    def get_queryset(self):
        user = self.request.user
        queryset = Team.objects.filter(brigadir__address__city=user.address.city)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.TEAM_LIST[APP_NAMES.NAME]
        return context
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View
from django.http import JsonResponse

import APP_NAMES
from profile.models import Status
from .models import CustomUser, Order

app_name = APP_NAMES.ORDERS[APP_NAMES.NAME]
verbose_name = APP_NAMES.ORDERS[APP_NAMES.VERBOSE]


class OrderListView(ListView):
    model = Order
    template_name = f'{APP_NAMES.ORDERS[APP_NAMES.NAME]}/index.html'
    context_object_name = 'order_list'
    ordering = ['-timestamp']

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(customer__address__city=user.address.city,master=None)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.ORDERS[APP_NAMES.NAME]
        return context


class TakeOrderView(View):
    def post(self, request, *args, **kwargs):

        orderId = request.POST.get('orderId')
        print("Получил запрос",request.POST)
        if orderId:
            user_id = self.request.user.pk
            user = get_object_or_404(CustomUser, pk=user_id)

            status = user.status
            if status.name == 'Мастер':
                new_status = Status.objects.get(name='Прораб')
                user.status = new_status
                user.save()

            # order = get_object_or_404(Order, customer_id=customer_id, master=None)
            order = Order.objects.get(id=orderId)
            order.master= request.user
            order.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'User ID is missing'}, status=400)




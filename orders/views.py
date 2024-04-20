from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View
from django.http import JsonResponse

import APP_NAMES
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
        queryset = Order.objects.filter(customer__address__city=user.address.city)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.ORDERS[APP_NAMES.NAME]
        return context



class TakeOrderView(View):

    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get('customer_id')
        if customer_id:
            order = get_object_or_404(Order, customer_id=customer_id, master=None)
            order.master_id = request.user.id
            order.save()


            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'User ID is missing'}, status=400)

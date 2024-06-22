from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic import TemplateView, View
from django.utils.safestring import mark_safe
import json
import APP_NAMES
from orders.models import Order
from profile.models import CustomUser


class MessageView(TemplateView):
    template_name = f'{APP_NAMES.MESSAGE[APP_NAMES.NAME]}/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender = context['view'].request.user.username
        context['sender'] = sender
        context['sender_id'] = context['view'].request.user.id
        context['page_style'] = APP_NAMES.MESSAGE[APP_NAMES.NAME]
        context['recipient'] = self.kwargs.get('recipient')
        if self.request.user.status.name == 'Заказ':
            order = Order.objects.get(customer=self.request.user)
            if order is not None:
                context['order_master'] = order.master
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['receiver_id'] = request.POST.get('receiver_id')
        return self.render_to_response(context)

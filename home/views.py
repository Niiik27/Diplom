from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

import APP_NAMES
from APP_NAMES import *
# from .forms import ArticleForm, BookForm, CustomUserCreationForm
# from .models import Article, Book, CustomUser, Team

class HomeTempateView(TemplateView):
    template_name = f'{APP_NAMES.HOME[APP_NAMES.NAME]}/index.html'
    # model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_style'] = APP_NAMES.HOME[APP_NAMES.NAME]
        return context
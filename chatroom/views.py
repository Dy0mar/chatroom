# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import (
    logout as auth_logout, authenticate, login as auth_login
)

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from .forms import RegistrationForm


class IndexView(TemplateView):
    template_name = 'chatroom/chatroom.html'


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'You have been logged out')
    return redirect(reverse('login'))


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST.copy())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(
                request, username=username, password=raw_password
            )
            auth_login(request, user)
            return redirect('home-page')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

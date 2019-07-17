# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import (
    logout as auth_logout, authenticate, login as auth_login
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView

from .forms import RegistrationForm, UserForm


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


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    template_name = 'registration/user_profile.html'

    def get_success_url(self):
        messages.success(self.request, 'Update!')
        return reverse_lazy('profile', kwargs={'username': self.object.username})

    def get_object(self, queryset=None):
        return self.model.objects.get(username=self.request.user)

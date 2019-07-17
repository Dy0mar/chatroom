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

from chatroom.models import ChatMessage
from .forms import RegistrationForm, UserForm


class IndexView(TemplateView):
    template_name = 'chatroom/chatroom.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        queryset = ChatMessage.objects.order_by("-created")[:10]
        count_messages = len(queryset)

        if count_messages > 0:
            current_message_id = queryset[count_messages - 1].id
            previous_message_id = ChatMessage.objects.filter(
                pk__lt=current_message_id
            ).order_by("-pk").first().id
        else:
            previous_message_id = -1

        context['chat_messages'] = reversed(queryset)
        context['previous_message_id'] = previous_message_id
        return context


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

# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Required')
    email = forms.EmailField(
        max_length=30, help_text='Required. Inform a valid email address.',
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(email=email).exclude(username=username)

        if email and qs.exists():
            raise forms.ValidationError(u'Email address already exists.')

        return email

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.instance.username
        qs = User.objects.filter(email=email).exclude(username=username)

        if email and email != self.instance.email and qs.exists():
            raise forms.ValidationError(u'Email address already exists.')

        return email

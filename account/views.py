from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import SignupForm


class Signup(CreateView):
    model = get_user_model()
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')


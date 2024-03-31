from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import auth

from .forms import SignupForm


class Signup(CreateView):
    model = get_user_model()
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')
    
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('login')


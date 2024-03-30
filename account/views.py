from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model

from .forms import SignupForm

def signup(request):
    form = SignupForm()
    return render(request, 'registraion/signup.html' , {'form': form})

# class Signup(CreateView):
#     model = get_user_model()
#     template_name = 'registration/signup.html'
#     form_class = SignupForm()


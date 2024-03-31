from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class SignupForm(UserCreationForm):
    
    password1 = forms.CharField(label='Password',
            widget=forms.PasswordInput(attrs={'class': "form-control", 'id': "password", 
            'placeholder': "Password", 'onfocus': "this.placeholder = ''", 'onblur': "this.placeholder = 'Password'"}))
    password2 = forms.CharField(label='Confirm Password',
            widget=forms.PasswordInput(attrs={'class': "form-control", 'id': "confirmPassword", 
            'placeholder': "Confirm Password", 'onfocus': "this.placeholder = ''", 'onblur': "this.placeholder = 'Confirm Password'"}))
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control", 'id': "name", 
             'placeholder': "Username", 'onfocus': "this.placeholder = ''", 'onblur': "this.placeholder = 'Username'"}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': "form-control", 'id': "email", 
             'placeholder': "Email Address", 'onfocus': "this.placeholder = ''", 'onblur': "this.placeholder = 'Email Address'"})
        }
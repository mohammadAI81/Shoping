from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('logout/', views.logout, name='logout'),
]

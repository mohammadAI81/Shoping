from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('callback/', views.payment_callback, name='callback'),
    path('confirmation/<int:ref_id>', views.info_payment, name='info-payment'),
]
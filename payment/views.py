from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib import messages
from django.db.models import Prefetch, F

import requests
import json
    
from cart.models import Order, OrderItem   


def payment_process(request):
    order = get_object_or_404(Order.objects.select_related('name'), name=request.user, status='u')
    total_price = order.get_total_price() * 50000
    
    request_header = {
        'accept': 'applications/json',
        'content-type': 'application/json',
    }
    
    request_data = {
        'MerchantID': 'aaancdksaaancdksaaancdksaaancdksmoc4',
        'Amount': float(total_price),
        'Description': f'# {order.id}: {order.name.username}',
        'CallbackURL': 'http://127.0.0.1:8000' + reverse('payment:callback')
    }

    zarinpall_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
    req = requests.post(url=zarinpall_url, data=json.dumps(request_data), headers=request_header)
    
    data = req.json()
    if 'errors' not in data:
        order.authority = data.get('Authority')
        order.save()
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{}'.format(data.get('Authority')))
    else:
        return HttpResponseBadRequest('errors from zarinpal')
    

def payment_callback(request):
    status = request.GET.get('Status')
    authority = request.GET.get('Authority')
    order = get_object_or_404(Order.objects.select_related('name'), authority=authority)

    total_price = order.get_total_price() * 50000
    
    if status == 'OK':
        
        request_headers = {
            'accept': 'applications/json',
            'content-type': 'application/json',
        }
        
        request_data = {
            'MerchantID': 'aaancdksaaancdksaaancdksaaancdksmoc4',
            'Amount': float(total_price),
            'Authority': authority
        }
        
        zarinpall_verify_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'
        
        req = requests.post(url=zarinpall_verify_url, data=json.dumps(request_data), headers=request_headers)
        data = req.json()
        print(data)
        
        if 'errors' not in data:
            status = data.get('Status')
            ref_id = data.get('RefID')
            if status == 100:
                order.ref_id = ref_id
                order.status = 'p'
                order.save()
                messages.success(request, 'cart is paid')
            elif status == 101:
                messages.success(request, 'your cart is payed')
            
            return redirect('payment:info-payment', ref_id)
        else:
            return HttpResponse('No payed')
    elif status == 'NOK':
        order.status = 'c'
        order.save()
        return HttpResponse('No payed')
    else:
        return HttpResponse('Unknow')
        

def info_payment(request, ref_id):
    order = get_object_or_404(Order.objects.prefetch_related(Prefetch(
                                                    'items',
                                                    queryset=OrderItem.objects.select_related('product') \
                                                        .annotate(total_price_product=F('unit_price') * F('quantity'))
                                                    )), ref_id=ref_id)
    return render(request, 'payment/confirmation.html', {'order': order})

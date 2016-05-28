from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


from forms import PaymentForm, ConfirmationForm
from configuration import secret_key

import hmac
import base64
import hashlib


# Create your views here.


def home(request):
    # The view for home page
    page_title = "Home"
    return render_to_response('home.html', {'page_title': page_title}, context_instance=RequestContext(request))


def pay(request):
    # The view for submitting payment data
    page_title = "Payment"
    payment_form = PaymentForm()
    return render_to_response('pay.html', {'page_title': page_title, 'payment_form': payment_form}, context_instance=RequestContext(request))


def confirm(request):
    # The view for payment confirmation
    page_title = "Confirmation"
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            params_dict = get_posted_parameters(payment_form)
            signature = sign(params_dict)
            params_dict['signature'] = signature
            confirmation_form = ConfirmationForm(params_dict)
            return render_to_response('confirm.html', {'page_title': page_title, 'confirmation_form': confirmation_form, 'params_dict': params_dict, 'signature': signature}, context_instance=RequestContext(request))
        else:
            from configuration import *
            page_title = "Payment"
            return render_to_response('pay.html', {'page_title': page_title, 'payment_form': payment_form}, context_instance=RequestContext(request))
    else:
        return pay(request)


@csrf_exempt
def receive(request):
    # The view containing the receipt
    page_title = "Receipt"
    if request.method == 'POST':
        posted = request.POST
        amount = posted['req_amount']
        return render_to_response('receive.html', {'page_title': page_title, 'posted': posted, 'amount': amount}, context_instance=RequestContext(request))
    else:
        return pay(request)


def sign(params_dict):
    # creates and returns the signature
    keys = params_dict['signed_field_names'].split(',')
    message = ','.join(['{key}={value}'.format(
        key=key, value=params_dict[key]) for key in keys])
    message = message.encode('utf-8')
    secret = secret_key.encode('utf-8')
    digested = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digested).decode()
    return signature


def get_posted_parameters(form):
    # places posted parameters in a dictionary and returns the dictionary
    return {field: form.cleaned_data[field] for field in form.cleaned_data}

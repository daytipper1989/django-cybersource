from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from forms import *
from django.views.decorators.csrf import csrf_exempt
import hmac
import base64
import hashlib

from configuration import secretKey

# Create your views here.


def home(request):
    #The view for home page
    pageTitle = "Home"
    return render_to_response('home.html', {'pageTitle': pageTitle}, context_instance=RequestContext(request))


def pay(request):
    #The view for submitting payment data
    pageTitle = "Payment"
    paymentForm = PaymentForm()
    return render_to_response('pay.html', {'pageTitle': pageTitle, 'paymentForm': paymentForm}, context_instance=RequestContext(request))


def confirm(request):
    #The view for payment confirmation
    pageTitle = "Confirmation"
    if request.method == 'POST':
        paymentForm = PaymentForm(request.POST)
        if paymentForm.is_valid():
            paramsDict = getPostedParameters(paymentForm)
            signature = sign(paramsDict)
            paramsDict['signature'] = signature
            confirmationForm = ConfirmationForm(paramsDict)
            return render_to_response('confirm.html', {'pageTitle': pageTitle, 'confirmationForm': confirmationForm, 'paramsDict': paramsDict, 'signature': signature}, context_instance=RequestContext(request))
        else:
            from configuration import *
            pageTitle = "Payment"
            return render_to_response('pay.html', {'pageTitle': pageTitle, 'paymentForm': paymentForm }, context_instance=RequestContext(request))
    else:
        return pay(request)

@csrf_exempt
def receive(request):
    #The view containing the receipt
    pageTitle = "Receipt"
    if request.method == 'POST':
        posted = request.POST
        amount = posted['req_amount']
        return render_to_response('receive.html', {'pageTitle':pageTitle,'posted':posted,'amount':amount}, context_instance=RequestContext(request))
    else:
        return pay(request)


def sign(paramsDict):
    #creates and returns the signature
    keys = paramsDict['signed_field_names'].split(',')
    message = ','.join(['{key}={value}'.format(key=key, value=paramsDict[key]) for key in keys])
    messageBeforeEncoding = message
    message = message.encode('utf-8')
    secret = secretKey.encode('utf-8')
    digested = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digested)#.decode()
    return signature

def getPostedParameters(paymentForm):
    #places posted parameters in a dictionary and returns the dictionary
    paramsDict = {}
    paramsDict['access_key'] = paymentForm.cleaned_data['access_key']
    paramsDict['profile_id'] = paymentForm.cleaned_data['profile_id']
    paramsDict['transaction_uuid'] = paymentForm.cleaned_data['transaction_uuid']
    paramsDict['signed_field_names'] = paymentForm.cleaned_data['signed_field_names']
    paramsDict['unsigned_field_names'] = paymentForm.cleaned_data['unsigned_field_names']
    paramsDict['signed_date_time'] = paymentForm.cleaned_data['signed_date_time']
    paramsDict['locale'] = paymentForm.cleaned_data['locale']
    paramsDict['transaction_type'] = paymentForm.cleaned_data['transaction_type']
    #paramsDict['bill_address1'] = paymentForm.cleaned_data['bill_address1']
    #paramsDict['bill_city'] = paymentForm.cleaned_data['bill_city']
    #paramsDict['bill_country'] = paymentForm.cleaned_data['bill_country']
    #paramsDict['customer_email'] = paymentForm.cleaned_data['customer_email']
    #paramsDict['customer_lastname'] = paymentForm.cleaned_data['customer_lastname']
    paramsDict['reference_number'] = paymentForm.cleaned_data['reference_number']
    paramsDict['amount'] = paymentForm.cleaned_data['amount']
    paramsDict['currency'] = paymentForm.cleaned_data['currency']
    paramsDict['ignore_avs'] = paymentForm.cleaned_data['ignore_avs']
    return paramsDict

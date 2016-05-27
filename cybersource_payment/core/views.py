from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from forms import *
from django.views.decorators.csrf import csrf_exempt
import datetime
import uuid
import hmac
import base64
import hashlib

secretKey = "b16669f97a9c4e4ab397cb8f75bc0765fdd99ca1c75445259d8947424dc83cd04fa04e0187424247b58895e22f1053cab9ce3d8b0b9b48f2bd357a5496c78f6c2e5c0c8e96c44603b8391a214aa046a06db5f41ecbbc4ba1ac1af5061f94a5e3f15db714e8c1496caa849f3b7b6dbf487f2ff4d9d3b84bac8bbb95f15f3e4180"

# Create your views here.


def home(request):
    pageTitle = "Home"
    return render_to_response('home.html', {'pageTitle': pageTitle}, context_instance=RequestContext(request))


def pay(request):
    from configuration import *
    pageTitle = "Payment"
    paymentForm = PaymentForm()
    uuID = str(uuid.uuid1())  # .replace("-", "")
    utcDateTime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return render_to_response('pay.html', {'pageTitle': pageTitle, 'paymentForm': paymentForm, 'uuID': uuID, 'utcDateTime': utcDateTime, 'profileID': profileID, 'accessKey': accessKey}, context_instance=RequestContext(request))


def confirm(request):
    pageTitle = "Confirmation"
    if request.method == 'POST':
        paymentForm = PaymentForm(request.POST)
        if paymentForm.is_valid():
            paramsDict = {}
            paramsDict['access_key'] = request.POST['access_key']
            paramsDict['profile_id'] = request.POST['profile_id']
            paramsDict['transaction_uuid'] = request.POST['transaction_uuid']
            paramsDict['signed_field_names'] = request.POST['signed_field_names']
            # paramsDict['unsigned_field_names'] = "payment_method,card_type,card_number,card_expiry_date,card_cvn,bill_to_forename,bill_to_surname,bill_to_email,bill_to_address_line1,bill_to_address_city,bill_to_address_postal_code,bill_to_address_state,bill_to_address_country"
            # paramsDict['unsigned_field_names']="bill_to_forename,bill_to_surname,bill_to_email,bill_to_address_line1,bill_to_address_state,bill_to_address_country,payment_method,driver_license_state,driver_license_number,date_of_birth,echeck_account_type,company_tax_id,echeck_sec_code,echeck_account_number,echeck_routing_number"
            paramsDict['unsigned_field_names'] = request.POST['unsigned_field_names']
            paramsDict['signed_date_time'] = request.POST['signed_date_time']
            paramsDict['locale'] = request.POST['locale']
            paramsDict['transaction_type'] = paymentForm.cleaned_data[
                'transaction_type']
            paramsDict['reference_number'] = paymentForm.cleaned_data[
                'reference_number']
            paramsDict['amount'] = paymentForm.cleaned_data['amount']
            paramsDict['currency'] = paymentForm.cleaned_data['currency']
            keys = paramsDict['signed_field_names'].split(',')
            message = ','.join(['{key}={value}'.format(
                key=key, value=paramsDict[key]) for key in keys])
            messageBeforeEncoding = message
            message = message.encode('utf-8')
            secret = secretKey.encode('utf-8')
            signature = base64.b64encode(
                hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()).decode()
            return render_to_response('confirm.html', {'pageTitle': pageTitle, 'paymentForm': paymentForm, 'paramsDict': paramsDict, 'messageBeforeEncoding': messageBeforeEncoding, 'signature': signature}, context_instance=RequestContext(request))
        else:
            from configuration import *
            pageTitle = "Payment"
            #paymentForm = PaymentForm()
            uuID = str(uuid.uuid1()).replace("-", "")
            utcDateTime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            return render_to_response('pay.html', {'pageTitle': pageTitle, 'paymentForm': paymentForm, 'uuID': uuID, 'utcDateTime': utcDateTime, 'profileID': profileID, 'accessKey': accessKey}, context_instance=RequestContext(request))
    else:
        return pay(request)

@csrf_exempt
def receive(request):
    pageTitle = "Receipt"
    if request.method == 'POST':
        d = request.POST
        amount = d['req_amount']
        return render_to_response('receive.html', {'pageTitle':pageTitle,'d':d,'amount':amount}, context_instance=RequestContext(request))
    else:
        return pay(request)

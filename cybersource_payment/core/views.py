from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
import uuid



# Create your views here.
def pay(request):
	from configuration import *
	pageTitle="Payment"
	uuID = str(uuid.uuid1()).replace("-","")
	utcDateTime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
	return render_to_response('pay.html', locals(), context_instance = RequestContext(request))
	
def confirm(request):
	pageTitle="Confirmation"
	paramsDict = {}
	paramsDict['access_key']=request.POST['access_key']
	paramsDict['profile_id']=request.POST['profile_id']
	paramsDict['transaction_uuid']=request.POST['transaction_uuid']
	paramsDict['signed_field_names']=request.POST['signed_field_names']
	paramsDict['unsigned_field_names']=request.POST['unsigned_field_names']
	paramsDict['signed_date_time']=request.POST['signed_date_time']
	paramsDict['locale']=request.POST['locale']
	paramsDict['transaction_type']=request.POST['transaction_type']
	paramsDict['reference_number']=request.POST['reference_number']
	paramsDict['amount']=request.POST['amount']
	paramsDict['currency']=request.POST['currency']
	return render_to_response('confirm.html', locals(), context_instance = RequestContext(request))
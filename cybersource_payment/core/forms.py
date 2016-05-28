from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from models import Confirmation
import time
import datetime
import uuid
from configuration import accessKey, profileID


class PaymentForm(forms.Form):
    transaction_type = forms.CharField(label=_('Transaction Type'), max_length=25, required=True, initial="authorization", disabled=True)
    reference_number = forms.CharField(label=_('Reference Number'), max_length=25, required=True, initial=str(int(round(time.time() * 1000))), disabled=True)
    amount = forms.DecimalField(label=_('Amount'), required=True, min_value=0.1, decimal_places=2, max_value=1000000)
    currency = forms.CharField(label=_('Currency'), max_length=25, required=True, initial="USD", disabled=True)
    bill_address1 = forms.CharField(label=_('First Address'), required=True, initial = "1 My Apartment", disabled = True)
    bill_city = forms.CharField(label=_('City'), required=True, initial = "Mountain View", disabled = True)
    bill_country = forms.CharField(label=_('Country'), required=True, initial = "US", disabled = True)
    customer_email = forms.CharField(label=_('Email'), required=True, initial = "joesmith@example.com", disabled = True)
    customer_lastname = forms.CharField(label=_('Last Name'), required=True, initial = "Smith", disabled = True)
    access_key = forms.CharField(label=_('Access Key'), required=True, initial = accessKey, disabled = True,widget = forms.HiddenInput())
    profile_id = forms.CharField(label=_('Profile ID'), required=True, initial = profileID, disabled = True,widget = forms.HiddenInput())
    transaction_uuid = forms.CharField(label=_('Transaction UUID'), required=True, initial = str(uuid.uuid1()), disabled = True,widget = forms.HiddenInput())
    #ignore_avs = forms.CharField(label=_('Ignore AVS'), required=True, initial = 'true', disabled = True,widget = forms.HiddenInput())
    signed_field_names = forms.CharField(label=_('Signed Field Names'), required=True, initial = "access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency", disabled = True,widget = forms.HiddenInput())
    unsigned_field_names = forms.CharField(label=_('Unsigned Field Names'), required=False, initial = "bill_address1,bill_city,bill_country,customer_email,customer_lastname", disabled = True,widget = forms.HiddenInput())
    #unsigned_field_names = forms.CharField(label=_('Unsigned Field Names'), required=False, initial = "", disabled = True,widget = forms.HiddenInput())
    signed_date_time = forms.CharField(label=_('Signed Datetime'), required=True, initial = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), disabled = True,widget = forms.HiddenInput())
    locale = forms.CharField(label=_('Locale'), required=True, initial = "en", disabled = True,widget = forms.HiddenInput())

class ConfirmationForm(ModelForm):

    class Meta:
        model = Confirmation
        fields = [
            'transaction_type',
            'reference_number',
            'amount',
            'currency',
            'bill_address1',
            'bill_city',
            'bill_country',
            'customer_email',
            'customer_lastname',
            'access_key',
            'profile_id',
            'transaction_uuid',
            'signed_field_names',
            'unsigned_field_names',
            'signed_date_time',
            'locale',
            'signature',
            #'ignore_avs',
        ]
    

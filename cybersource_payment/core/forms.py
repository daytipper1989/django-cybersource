from django import forms
from django.utils.translation import ugettext_lazy as _
import time


class PaymentForm(forms.Form):
    transaction_type = forms.CharField(label=_(
        'Transaction Type'), max_length=25, required=True, initial="authorization", disabled=True)
    reference_number = forms.CharField(label=_('Reference Number'), max_length=25, required=True, initial=str(
        int(round(time.time() * 1000))), disabled=True)
    amount = forms.DecimalField(label=_(
        'Amount'), required=True, min_value=0.1, decimal_places=2, max_value=1000000)
    currency = forms.CharField(
        label=_('Currency'), max_length=25, required=True, initial="USD", disabled=True)

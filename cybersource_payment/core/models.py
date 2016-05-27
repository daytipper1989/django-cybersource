from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Confirmation(models.Model):
    access_key  = models.CharField(_('Access Key'),max_length=255,null=False,blank=False)
    profile_id = models.CharField(_('Profile ID'),max_length=255,null=False,blank=False)
    transaction_uuid = models.CharField(_('Transaction UUID'),max_length=255,null=False,blank=False)
    signed_field_names = models.TextField(_('Signed Field Names'),max_length=255,null=False,blank=False)
    unsigned_field_names = models.TextField(_('Unsigned Field Names'),max_length=255,null=True,blank=True)
    signed_date_time = models.CharField(_('Signed Datetime'),max_length=255,null=False,blank=False)
    locale = models.CharField(_('Locale'),max_length=255,null=False,blank=False)
    transaction_type = models.CharField(_('Transaction Type'),max_length=255,null=False,blank=False)
    #bill_address1 = models.CharField(_('Bill Address 1'),max_length=255,null=False,blank=False)
    #bill_city = models.CharField(_('Bill City'),max_length=255,null=False,blank=False)
    #bill_country = models.CharField(_('Bill Country'),max_length=255,null=False,blank=False)
    #customer_email = models.CharField(_('Customer Email'),max_length=255,null=False,blank=False)
    #customer_lastname = models.CharField(_('Customer Last Name'),max_length=255,null=False,blank=False)
    reference_number = models.CharField(_('Reference Number'),max_length=255,null=False,blank=False)
    amount = models.CharField(_('Amount'),max_length=255,null=False,blank=False)
    currency = models.CharField(_('Currency'),max_length=255,null=False,blank=False)
    signature = models.CharField(_('Signature'),max_length=255,null=False,blank=False)
    ignore_avs = models.CharField(_('Ignore AVS'),max_length=255,null=False,blank=False)

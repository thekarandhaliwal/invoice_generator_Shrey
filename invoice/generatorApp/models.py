from django.db import models

# Create your models here.
# models.py
from django.db import models

class BankDetail(models.Model):
    beneficiary_name = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    micr_code = models.CharField(max_length=20, blank=True, null=True)


from django.urls import path
from . views import invoice_view, bank_details_form

urlpatterns = [
    path("invoice/", invoice_view, name="invoice_view"),
    path("bank-details/", bank_details_form, name="bank_details_form"),
]

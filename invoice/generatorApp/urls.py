from django.urls import path
from . views import invoice_view, bank_details_form, custom_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("Create-Invoice/", invoice_view, name="invoice_view"),
    path("bank-details/", bank_details_form, name="bank_details_form"),
]

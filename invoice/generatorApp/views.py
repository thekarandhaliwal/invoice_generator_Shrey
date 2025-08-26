from django.shortcuts import render

# Create your views here.
import pdfkit
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import date

# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("invoice_view")  # redirect to dashboard after login
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    
    return render(request, "registration/login.html", {"form": form})


def index(request):
    return render(request, "base.html")

# def invoice_view(request):
#     bank = BankDetail.objects.last()
#     if request.method == "POST":
#         client_name = request.POST['client_name']
#         email = request.POST['email']
#         invoice_no = request.POST['invoice_no']

#         html = render_to_string("invoice_template.html", {
#             "client_name": client_name,
#             "email": email,
#             "invoice_no": invoice_no,
#             "date": date.today()
#         })

#         options = {
#             'margin-top': '0mm',
#             'margin-right': '0mm',
#             'margin-bottom': '0mm',
#             'margin-left': '0mm',
#             'enable-local-file-access': None
#         }

#         pdf = pdfkit.from_string(html, False, options=options)

#         response = HttpResponse(pdf, content_type="application/pdf")
#         response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_no}.pdf"'
#         return response

#     return render(request, "invoice_form.html", {"bank": bank})


import pdfkit
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from datetime import date
from .models import BankDetail
from django.conf import settings
import os

from django.contrib.auth.decorators import login_required

# @login_required
# def invoice_view(request):
#     bank = BankDetail.objects.last()   # fetch last saved bank detail

#     if request.method == "POST":
#         invoice_no = request.POST.get("invoice_no")
#         invoice_date = request.POST.get("invoice_date")
#         client_name = request.POST.get("client_name")
#         client_address = request.POST.get("client_address")
#         contact_no = request.POST.get("contact_no")
#         email = request.POST.get("email")
#         gstin = request.POST.get("gstin")
#         ref_no = request.POST.get("ref_no")
#         ref_date = request.POST.get("ref_date")

#         sn_list = request.POST.getlist("sn[]")
#         topics = request.POST.getlist("training_topic[]")
#         venues = request.POST.getlist("venue[]")
#         participants = request.POST.getlist("participants[]")
#         dates = request.POST.getlist("training_date[]")
#         hsn_codes = request.POST.getlist("hsn_code[]")
#         fee_per_list = request.POST.getlist("course_fee_per_participant[]")
#         fee_amount_list = request.POST.getlist("course_fee_amount[]")

#         # Build rows for template
#         training_rows = []
#         total_before_tax = 0
#         for i in range(len(sn_list)):
#             row = {
#                 "sn": sn_list[i],
#                 "topic": topics[i],
#                 "venue": venues[i],
#                 "participants": participants[i],
#                 "date": dates[i],
#                 "hsn": hsn_codes[i],
#                 "fee_per": fee_per_list[i],
#                 "fee_amount": fee_amount_list[i],
#             }
#             training_rows.append(row)
#             try:
#                 total_before_tax += float(fee_amount_list[i] or 0)
#             except:
#                 pass

#         igst = total_before_tax * 0.18
#         total_after_tax = total_before_tax + igst

#         context = {
#             "invoice_no": invoice_no,
#             "invoice_date": invoice_date or date.today(),
#             "client_name": client_name,
#             "client_address": client_address,
#             "contact_no": contact_no,
#             "email": email,
#             "gstin": gstin,
#             "ref_no": ref_no,
#             "ref_date": ref_date,

#             "trainings": training_rows,
#             "total_before_tax": f"{total_before_tax:,.2f}",
#             "igst": f"{igst:,.2f}",
#             "total_after_tax": f"{total_after_tax:,.2f}",
#             "grand_total": f"{total_after_tax:,.2f}",


#             "bank": bank,
#         }


# from django.contrib.auth.decorators import login_required
# from num2words import num2words
# from datetime import date

# @login_required
# def invoice_view(request):
#     bank = BankDetail.objects.last()   # fetch last saved bank detail

#     if request.method == "POST":
#         invoice_no = request.POST.get("invoice_no")
#         invoice_date = request.POST.get("invoice_date")
#         client_name = request.POST.get("client_name")
#         client_address = request.POST.get("client_address")
#         contact_no = request.POST.get("contact_no")
#         email = request.POST.get("email")
#         gstin = request.POST.get("gstin")
#         ref_no = request.POST.get("ref_no")
#         ref_date = request.POST.get("ref_date")

#         sn_list = request.POST.getlist("sn[]")
#         topics = request.POST.getlist("training_topic[]")
#         venues = request.POST.getlist("venue[]")
#         participants = request.POST.getlist("participants[]")
#         dates = request.POST.getlist("training_date[]")
#         hsn_codes = request.POST.getlist("hsn_code[]")
#         fee_per_list = request.POST.getlist("course_fee_per_participant[]")
#         fee_amount_list = request.POST.getlist("course_fee_amount[]")

#         # Build rows for template
#         training_rows = []
#         total_before_tax = 0
#         for i in range(len(sn_list)):
#             row = {
#                 "sn": sn_list[i],
#                 "topic": topics[i],
#                 "venue": venues[i],
#                 "participants": participants[i],
#                 "date": dates[i],
#                 "hsn": hsn_codes[i],
#                 "fee_per": fee_per_list[i],
#                 "fee_amount": fee_amount_list[i],
#             }
#             training_rows.append(row)
#             try:
#                 total_before_tax += float(fee_amount_list[i] or 0)
#             except:
#                 pass

#         igst = total_before_tax * 0.18
#         total_after_tax = total_before_tax + igst

#         # Convert to words (currency in Indian format)
#         grand_total_words = num2words(
#             round(total_after_tax, 2),
#             to="currency",
#             lang="en_IN"
#         ).replace("euro", "Rupees").replace("cents", "Paise")

#         context = {
#             "invoice_no": invoice_no,
#             "invoice_date": invoice_date or date.today(),
#             "client_name": client_name,
#             "client_address": client_address,
#             "contact_no": contact_no,
#             "email": email,
#             "gstin": gstin,
#             "ref_no": ref_no,
#             "ref_date": ref_date,

#             "trainings": training_rows,
#             "total_before_tax": f"{total_before_tax:,.2f}",
#             "igst": f"{igst:,.2f}",
#             "total_after_tax": f"{total_after_tax:,.2f}",
#             "grand_total": f"{total_after_tax:,.2f}",
#             "amount_words": grand_total_words,   # ✅ send to template

#             "bank": bank,
#         }



        # return render(request, "invoice_template.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from num2words import num2words
from datetime import date
from .models import BankDetail


# @login_required
# def invoice_view(request):
#     bank = BankDetail.objects.last()   # fetch last saved bank detail

#     if request.method == "POST":
#         invoice_no = request.POST.get("invoice_no")
#         invoice_date = request.POST.get("invoice_date")
#         client_name = request.POST.get("client_name")
#         client_address = request.POST.get("client_address")
#         contact_no = request.POST.get("contact_no")
#         email = request.POST.get("email")
#         gstin = request.POST.get("gstin")
#         ref_no = request.POST.get("ref_no")
#         ref_date = request.POST.get("ref_date")

#         sn_list = request.POST.getlist("sn[]")
#         topics = request.POST.getlist("training_topic[]")
#         venues = request.POST.getlist("venue[]")
#         participants = request.POST.getlist("participants[]")
#         dates = request.POST.getlist("training_date[]")
#         hsn_codes = request.POST.getlist("hsn_code[]")
#         fee_per_list = request.POST.getlist("course_fee_per_participant[]")
#         fee_amount_list = request.POST.getlist("course_fee_amount[]")

#         # Build rows for template
#         training_rows = []
#         total_before_tax = 0
#         for i in range(len(sn_list)):
#             row = {
#                 "sn": sn_list[i],
#                 "topic": topics[i],
#                 "venue": venues[i],
#                 "participants": participants[i],
#                 "date": dates[i],
#                 "hsn": hsn_codes[i],
#                 "fee_per": fee_per_list[i],
#                 "fee_amount": fee_amount_list[i],
#             }
#             training_rows.append(row)
#             try:
#                 total_before_tax += float(fee_amount_list[i] or 0)
#             except:
#                 pass

#         # Tax calculation
#         igst = total_before_tax * 0.18
#         total_after_tax = total_before_tax + igst

#         # --- Bill Amount in Words ---
#         # Round to nearest rupee (ignore paise)
#         grand_total_number = int(round(total_after_tax, 0))

#         # Convert to words (Indian style)
#         grand_total_words = num2words(grand_total_number, lang="en_IN")
#         grand_total_words = grand_total_words.replace("-", " ").title() + " Only"

#         # Context for template
#         context = {
#             "invoice_no": invoice_no,
#             "invoice_date": invoice_date or date.today(),
#             "client_name": client_name,
#             "client_address": client_address,
#             "contact_no": contact_no,
#             "email": email,
#             "gstin": gstin,
#             "ref_no": ref_no,
#             "ref_date": ref_date,

#             "trainings": training_rows,
#             "total_before_tax": f"{total_before_tax:,.2f}",
#             "igst": f"{igst:,.2f}",
#             "total_after_tax": f"{total_after_tax:,.2f}",
#             "grand_total": f"{total_after_tax:,.2f}",
#             "grand_total_words": grand_total_words,   # ✅ words for display

#             "bank": bank,
#         }



@login_required
def invoice_view(request):
    bank = BankDetail.objects.last()   # fetch last saved bank detail

    if request.method == "POST":
        invoice_no = request.POST.get("invoice_no")
        invoice_date = request.POST.get("invoice_date")
        client_name = request.POST.get("client_name")
        client_address = request.POST.get("client_address")
        contact_no = request.POST.get("contact_no")
        email = request.POST.get("email")
        gstin = request.POST.get("gstin")
        ref_no = request.POST.get("ref_no")
        ref_date = request.POST.get("ref_date")
        gst_percentage = request.POST.get("gst_percentage")  # ✅ from frontend

        # default GST % if not entered
        try:
            gst_percentage = float(gst_percentage or 0)
        except:
            gst_percentage = 0

        sn_list = request.POST.getlist("sn[]")
        topics = request.POST.getlist("training_topic[]")
        venues = request.POST.getlist("venue[]")
        participants = request.POST.getlist("participants[]")
        dates = request.POST.getlist("training_date[]")
        hsn_codes = request.POST.getlist("hsn_code[]")
        fee_per_list = request.POST.getlist("course_fee_per_participant[]")
        fee_amount_list = request.POST.getlist("course_fee_amount[]")

        # Build rows for template
        training_rows = []
        total_before_tax = 0
        for i in range(len(sn_list)):
            row = {
                "sn": sn_list[i],
                "topic": topics[i],
                "venue": venues[i],
                "participants": participants[i],
                "date": dates[i],
                "hsn": hsn_codes[i],
                "fee_per": fee_per_list[i],
                "fee_amount": fee_amount_list[i],
            }
            training_rows.append(row)
            try:
                total_before_tax += float(fee_amount_list[i] or 0)
            except:
                pass

        # Tax calculation (user entered GST %)
        gst_amount = total_before_tax * (gst_percentage / 100)
        total_after_tax = total_before_tax + gst_amount

        # --- Bill Amount in Words ---
        grand_total_number = int(round(total_after_tax, 0))
        grand_total_words = num2words(grand_total_number, lang="en_IN")
        grand_total_words = grand_total_words.replace("-", " ").title() + " Only"

        # Context for template
        context = {
            "invoice_no": invoice_no,
            "invoice_date": invoice_date or date.today(),
            "client_name": client_name,
            "client_address": client_address,
            "contact_no": contact_no,
            "email": email,
            "gstin": gstin,
            "ref_no": ref_no,
            "ref_date": ref_date,

            "trainings": training_rows,
            "total_before_tax": f"{total_before_tax:,.2f}",
            "gst_percentage": gst_percentage,
            "gst_amount": f"{gst_amount:,.2f}",
            "total_after_tax": f"{total_after_tax:,.2f}",
            "grand_total": f"{total_after_tax:,.2f}",
            "grand_total_words": grand_total_words,

            "bank": bank,
        }
        
        html = render_to_string("invoice_template.html", context)

        static_dir = os.path.join(settings.BASE_DIR, 'generatorApp', 'static')  # Adjust 'planets' if needed
        html = html.replace('/static/', f'file://{static_dir}/')

        options = {
            'margin-top': '2mm',
            'margin-right': '5mm',
            'margin-bottom': '0mm',
            'margin-left': '5mm',
            'enable-local-file-access': None
        }

        # Generate PDF
        pdf = pdfkit.from_string(html, False, options=options)

        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_no}.pdf"'
        return response

    return render(request, "invoice_form.html", {"bank": bank})

from django.shortcuts import render, redirect
from .models import BankDetail

def bank_details_form(request):
    if request.method == "POST":
        BankDetail.objects.all().delete()
        BankDetail.objects.create(
            beneficiary_name=request.POST['beneficiary_name'],
            bank_name=request.POST['bank_name'],
            branch=request.POST['branch'],
            account_number=request.POST['account_number'],
            ifsc_code=request.POST['ifsc_code'],
            micr_code=request.POST.get('micr_code', "")
        )
        return redirect('invoice_view')
    return render(request, "bank_details_form.html")

# def invoice_page(request):
#     bank = BankDetail.objects.last()
#     return render(request, "invoice.html", {"bank": bank})

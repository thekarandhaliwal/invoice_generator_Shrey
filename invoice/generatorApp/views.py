from django.shortcuts import render

# Create your views here.
import pdfkit
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import date

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

        # training_topic = request.POST.get("training_topic")
        # venue = request.POST.get("venue")
        # participants = request.POST.get("participants")
        # training_date = request.POST.get("training_date")
        # hsn_code = request.POST.get("hsn_code")
        # fee_per_participant = request.POST.get("fee_per_participant")
        # fee_amount = request.POST.get("fee_amount")

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

        # Tax calculations
        igst = total_before_tax * 0.18
        total_after_tax = total_before_tax + igst


        # total_before_tax = request.POST.get("total_before_tax")
        # igst = request.POST.get("igst")
        # total_after_tax = request.POST.get("total_after_tax")
        # amount_words = request.POST.get("amount_words")
        # grand_total = request.POST.get("grand_total")

        # context = {
        #     "invoice_no": invoice_no,
        #     "invoice_date": invoice_date or date.today(),
        #     "client_name": client_name,
        #     "client_address": client_address,
        #     "contact_no": contact_no,
        #     "email": email,
        #     "gstin": gstin,
        #     "ref_no": ref_no,
        #     "ref_date": ref_date,

        #     "training_topic": training_topic,
        #     "venue": venue,
        #     "participants": participants,
        #     "training_date": training_date,
        #     "hsn_code": hsn_code,
        #     "fee_per_participant": fee_per_participant,
        #     "fee_amount": fee_amount,

        #     "total_before_tax": total_before_tax,
        #     "igst": igst,
        #     "total_after_tax": total_after_tax,
        #     "amount_words": amount_words,
        #     "grand_total": grand_total,

        #     "bank": bank,   # pass latest saved bank details
        # }

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

            # "trainings": trainings,  # 👈 now loop in template
            "trainings": training_rows,
            "total_before_tax": f"{total_before_tax:,.2f}",
            "igst": f"{igst:,.2f}",
            "total_after_tax": f"{total_after_tax:,.2f}",
            "grand_total": f"{total_after_tax:,.2f}",
            # "total_before_tax": request.POST.get("total_before_tax"),
            # "igst": request.POST.get("igst"),
            # "total_after_tax": request.POST.get("total_after_tax"),
            # "amount_words": request.POST.get("amount_words"),
            # "grand_total": request.POST.get("grand_total"),

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

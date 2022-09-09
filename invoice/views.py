from django.shortcuts import render
from invoice.models import Invoices, InvoiceItems
from django.db.models import Sum
from django.core.mail import EmailMessage
from django.template.loader import get_template
from config import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404


def get_invoice_context(invoice_number):
    invoice = Invoices.objects.get(number=invoice_number)
    invoice_item = InvoiceItems.objects.filter(invoice=invoice)
    total = InvoiceItems.objects.filter(invoice=invoice).aggregate(Sum('sub_total'))
    context = {
        'careplus_base_url': settings.WAGTAILADMIN_BASE_URL,
        'invoice': invoice,
        'invoice_item': invoice_item,
        'total': total['sub_total__sum'],
    }

    return invoice, context


@login_required
def print_invoice(request, invoice_number):
    invoice, context = get_invoice_context(invoice_number)

    if invoice.patient.email and not invoice.is_email:
        try:
            invoice.user.membership.is_clinic
            if invoice.user.membership.is_clinic:
                name_text = invoice.user.clinic_name
            else:
                name_text = invoice.user.first_name + ' ' + invoice.user.last_name

        except AttributeError:
            pass

        subject = '[CarePlus] Invoice from {}'.format(name_text)
        template = get_template('invoice/email_plain.html')
        content = template.render(context)
        msg = EmailMessage(
            subject, content,
            settings.EMAIL_HOST_USER, to=[invoice.patient.email, ]
        )
        msg.content_subtype = 'html'
        result = msg.send()
        if result:
            invoice.is_email = True
            invoice.save()

    return render(request, 'invoice/print_plain.html', context)


def html_invoice(request, invoice_number):
    invoice, context = get_invoice_context(invoice_number)

    if invoice.is_final:
        return render(request, 'invoice/browser.html', context)
    else:
        raise Http404('Not found!')

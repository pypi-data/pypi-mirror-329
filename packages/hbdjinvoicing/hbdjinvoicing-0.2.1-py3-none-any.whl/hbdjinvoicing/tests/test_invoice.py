import pytest

from ..models import Invoice, InvoiceLine, InvoiceVat, refresh_invoice

pytestmark = pytest.mark.django_db


def test_invoice_create():
    invoice = Invoice()
    invoice.number = "F0000-00-0000"
    invoice.payment_mode = "cash"

    invoice.clean()

    assert invoice.total_vat_excl == 0
    assert invoice.total_vat_incl == 0

    invoice.save()

    line = InvoiceLine()
    line.invoice = invoice
    line.title = "test"
    line.description = "test"
    line.quantity = 10
    line.unit_price = 10
    line.vat_rate = 20

    line.clean()

    assert line.price_vat_excl == 100
    assert line.price_vat_only == 20
    assert line.price_vat_incl == 120

    line.save()
    refresh_invoice(sender=InvoiceLine, instance=line)

    assert InvoiceVat.objects.filter(invoice=invoice, vat_rate=20, price=20).exists()

    invoice.refresh_from_db()

    assert invoice.total_vat_excl == 100
    assert invoice.total_vat_incl == 120

    invoice.total_vat_excl = 0
    invoice.total_vat_incl = 0

    invoice.clean()

    assert invoice.total_vat_excl == 100
    assert invoice.total_vat_incl == 120

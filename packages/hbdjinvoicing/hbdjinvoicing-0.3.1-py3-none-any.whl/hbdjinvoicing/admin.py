from django.contrib import admin
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin

from .models import Invoice, InvoiceLine, InvoiceVat, Organisation


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    readonly_fields = ["price_vat_excl", "price_vat_only", "price_vat_incl"]
    extra = 0


class InvoiceVatInline(admin.TabularInline):
    model = InvoiceVat
    readonly_fields = ["vat_rate", "price"]
    can_delete = False
    extra = 0

    def has_add_permission(self, *args):
        return False


class InvoiceHtmlView(DetailView):
    model = Invoice
    template_name = "hbdjinvoicing/pdf.html"


class InvoicePdfView(WeasyTemplateResponseMixin, InvoiceHtmlView):
    pdf_attachment = False

    def get_pdf_filename(self):
        return f"{self.object.name}_{self.object.number}.pdf"


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceLineInline, InvoiceVatInline]
    list_display = ["name", "date", "number", "total_vat_incl", "pdf_link"]
    search_fields = ["name", "date", "number", "total_vat_incl"]
    fields = [
        "pdf_link",
        "organisation",
        "number",
        "date",
        "payment_mode",
        "name",
        "street",
        "zipcode",
        "city",
        "country",
    ]
    readonly_fields = [
        "pdf_link",
        "total_vat_excl",
        "total_vat_incl",
    ]

    def pdf_link(self, obj):
        if not obj.pk:
            return ""
        path = reverse("admin:pdf", args=[obj.pk])
        return mark_safe(f'<a href="{path}">PDF</a>')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<path:pk>/pdf/",
                self.admin_site.admin_view(InvoicePdfView.as_view()),
                name="pdf",
            )
        ]
        return my_urls + urls


class OrganisationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Organisation, OrganisationAdmin)

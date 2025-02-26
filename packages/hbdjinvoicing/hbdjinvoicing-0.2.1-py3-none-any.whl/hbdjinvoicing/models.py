from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):  # noqa: DJ008
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        verbose_name=_("Date de création"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        verbose_name=_("Date de modification"),
    )

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    name = models.CharField()
    street = models.CharField()
    zipcode = models.CharField()
    city = models.CharField()
    country = models.CharField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


def organisation_logo_upload_to(instance, filename):
    return f"organisation/{instance.slug}/logo/{filename}"


class Organisation(AddressMixin):
    email = models.EmailField()
    logo = models.ImageField(upload_to=organisation_logo_upload_to)

    bottom_comment = models.TextField()

    legal_status = models.CharField()
    siren = models.CharField()
    siret = models.CharField()
    vat_id = models.CharField()

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.name)


def invoice_default_date():
    return now().date()


class Invoice(AddressMixin, BaseModel):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, null=True, default=None
    )
    number = models.CharField(unique=True)
    date = models.DateField(default=invoice_default_date)
    payment_mode = models.CharField()
    total_vat_excl = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    total_vat_incl = models.DecimalField(decimal_places=2, max_digits=9, default=0)

    def __str__(self):
        return f"{self.name} {self.number}"

    def clean(self):
        if not self.id:
            self.total_vat_excl = 0
            self.total_vat_incl = 0
        else:
            self.refresh_totals()

        super().save()

    def refresh_totals(self):
        self.total_vat_excl = sum(
            [line.price_vat_excl for line in self.invoiceline_set.all()]
        )
        self.total_vat_incl = sum(
            [line.price_vat_incl for line in self.invoiceline_set.all()]
        )

    def refresh_vat(self):
        rows = (
            self.invoiceline_set.values("vat_rate")
            .order_by("vat_rate")
            .annotate(price=Sum("price_vat_only"))
        )
        for row in rows:
            invoice_vat, created = self.invoicevat_set.get_or_create(
                vat_rate=row["vat_rate"], defaults={"price": row["price"]}
            )
            if not created:
                invoice_vat.price = row["price"]
                invoice_vat.save()


class InvoiceVat(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    vat_rate = models.DecimalField(decimal_places=2, max_digits=9)
    price = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return f"{self.invoice} vat {self.vat_rate} %"


class InvoiceLine(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    title = models.CharField()
    descritiption = models.CharField()
    quantity = models.DecimalField(decimal_places=2, max_digits=9)
    unit = models.CharField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=9)
    price_vat_excl = models.DecimalField(decimal_places=2, max_digits=9)
    vat_rate = models.DecimalField(decimal_places=2, max_digits=9)
    price_vat_only = models.DecimalField(decimal_places=2, max_digits=9)
    price_vat_incl = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return f"{self.invoice} line {self.id}"

    def clean(self):
        self.price_vat_excl = self.unit_price * self.quantity
        self.price_vat_only = self.price_vat_excl * self.vat_rate / 100
        self.price_vat_incl = self.price_vat_excl + self.price_vat_only

        super().clean()


@receiver(post_save, sender=InvoiceLine)
def refresh_invoice(sender, instance, **kwargs):
    instance.invoice.refresh_vat()
    instance.invoice.refresh_totals()
    instance.invoice.save()

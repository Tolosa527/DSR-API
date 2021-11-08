from django.db import models
from dsrs.static_messages import *


class Territory(models.Model):

    name = models.CharField(max_length=48, default=TERRITORY_DEFAULT_NAME, null=True)
    code_2 = models.CharField(
        max_length=2, default=TERRITORY_DEFAULT_CODE, primary_key=True
    )
    code_3 = models.CharField(max_length=2, null=True)
    local_currency = models.ForeignKey(
        "Currency",
        related_name="territories",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        db_table = "territory"
        verbose_name = "territory"
        verbose_name_plural = "territories"
        ordering = ("name",)


class Currency(models.Model):

    name = models.CharField(max_length=48, default=CURRENCY_DEFAULT_NAME, null=True)
    symbol = models.CharField(max_length=4, null=True)
    code = models.CharField(
        max_length=3, default=CURRENCY_DEFAULT_CODE, primary_key=True
    )

    class Meta:
        db_table = "currency"
        verbose_name = "currency"
        verbose_name_plural = "currencies"


class DSR(models.Model):
    class Meta:
        db_table = "dsr"

    id = models.IntegerField(null=False, primary_key=True)
    path = models.CharField(max_length=256, default=DEFAULT_PATH, null=False)
    period_start = models.DateField(null=False)
    period_end = models.DateField(null=False)
    status = models.CharField(
        choices=STATUS_ALL, default=STATUS_ALL[1][0], max_length=48, null=False
    )
    territory = models.ForeignKey(
        Territory, related_name="dsrs", on_delete=models.CASCADE, null=False
    )
    currency = models.ForeignKey(
        Currency, related_name="dsrs", on_delete=models.CASCADE, null=False
    )


class Resource(models.Model):
    class Meta:
        db_table = "resource"

    dsp_id = models.CharField(max_length=256, null=False)
    title = models.CharField(max_length=256, null=True)
    artists = models.CharField(max_length=256, null=True)
    isrc = models.CharField(max_length=256, null=True)
    usages = models.IntegerField()
    revenue = models.BigIntegerField()
    dsrs = models.ForeignKey(
        DSR, related_name="resource", on_delete=models.CASCADE, null=True
    )

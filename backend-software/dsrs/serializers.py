from rest_framework import serializers

from . import models


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Territory
        fields = (
            "name",
            "code_2",
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = (
            "name",
            "code",
        )


class DSRSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = models.DSR
        fields = (
            "id",
            "path",
            "period_start",
            "period_end",
            "status",
            "territory",
            "currency",
        )

    def create(self, data):
        print(**data)
        instance = models.DSR.objects.create(**data)
        return instance


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = (
            "dsp_id",
            "title",
            "artists",
            "isrc",
            "usages",
            "revenue",
        )

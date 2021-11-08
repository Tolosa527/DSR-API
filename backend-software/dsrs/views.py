import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from dsrs.utils import Utils
from dsrs.static_messages import messages
from dsrs.servicies.cache import get_redis_client
from digital import settings
from . import models, serializers


class DSRViewSet(viewsets.ReadOnlyModelViewSet):

    """
    DSR class
    """

    queryset = models.DSR.objects.all()
    serializer_class = serializers.DSRSerializer

    def list(self, request, *args, **kwargs):
        """
        Return a list of DSRS.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        updated_data = {"message": messages.get("dsr_list_success")}
        updated_data.update({"data": serializer.data})
        return Response(updated_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):

        """
        Return a DSR object select by id. If the object does not
        exist, return an error message with the status 404
        """

        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(*args, **kwargs)
            serializer = self.get_serializer(obj)
            updated_data = {"message": messages.get("dsr_detail_success")}
            updated_data.update({"data": serializer.data})
        except queryset.model.DoesNotExist:
            updated_data = {"message": messages.get("not found")}
            return Response(updated_data, status.HTTP_404_NOT_FOUND)

        return Response(updated_data, status.HTTP_200_OK)


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):

    """
    Resource class
    """

    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        TOP percentile by revenue:
        Returns the TOP percentile by revenue (inverse of percentile).

        For example, "top percentile 10" returns the unique resources by revenue that accounts
        10% of the total revenue.
        """
        utils = Utils()
        client = get_redis_client()
        rates_dict = {}
        resources = models.Resource.objects.all()
        percentile = int(kwargs.get("pk")) / 100

        if not client.get("rates"):
            rates_dict = utils.AnyCurrencyToEUR(
                [currency.code for currency in models.Currency.objects.all()]
            )
            client.set(
                "rates", json.dumps(rates_dict), ex=settings.REDIS_EXPIRATION_TIME
            )
        else:
            print("GETTING DATA FROM CACHE")
            rates_dict = json.loads(client.get("rates").decode("utf-8"))

        dict_resources = utils.get_dict_from_model(resources)
        result = utils.dataFrame_resource_process(
            dict_resources, rates_dict, percentile
        )
        result_serlized_data = utils.make_resource_payload(result)
        updated_data = {"message": messages.get("resources_found")}
        updated_data.update({"data": result_serlized_data})
        return Response(updated_data, status.HTTP_200_OK)

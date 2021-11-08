from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import DSR, Currency, Territory, Resource
from .. import utils


class DSRSTests(APITestCase):

    fixtures = ["db"]

    def test_dsrs_success(self):
        """
        Status code 200, list of DSR returned
        """
        response = self.client.get(reverse("dsr-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "An array of DSR in JSON format")
        self.assertGreater(len(response.data), 1)

    def test_dsrs_by_id_success(self):
        """
        Status code 200, DSR selected by ID
        """
        response = self.client.get(reverse("dsr-detail", args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "DSR found in JSON format")

    def test_dsrs_by_id_fail(self):
        """
        Status code 404, DSR selected by ID not found
        """
        response = self.client.get(reverse("dsr-detail", args=[1000]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get("message"), "DSR does not exist")


class ResourceTests(APITestCase):

    def test_resource_filtered_by_percentile(self):
        """
        Status code 200 and it returns the TOP percentile by revenue
        """
        response = self.client.get(reverse("resource-detail", args=[10]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get("message"),
            "List of resources in JSON format ordered by revenue in EURO",
        )

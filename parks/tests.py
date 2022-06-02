from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Park


class ParkTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_park = Park.objects.create(
            name="Yosemite",
            visitor=testuser1,
            location="East-Central California",
            description="The definitive California wilderness gem. You gotta see Half Dome!",
        )
        test_park.save()

    def test_parks_model(self):
        park = Park.objects.get(id=1)
        actual_visitor = str(park.visitor)
        actual_name = str(park.name)
        actual_location = str(park.location)
        actual_description = str(park.description)
        self.assertEqual(actual_visitor, "testuser1")
        self.assertEqual(actual_name, "Yosemite")
        self.assertEqual(actual_location, "East-Central California")
        self.assertEqual(
            actual_description, "The definitive California wilderness gem. You gotta see Half Dome!"
        )

    def test_get_park_list(self):
        url = reverse("park_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parks = response.data
        self.assertEqual(len(parks), 1)
        self.assertEqual(parks[0]["name"], "Yosemite")

    def test_get_park_by_id(self):
        url = reverse("park_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        park = response.data
        self.assertEqual(park["name"], "Yosemite")

    def test_create_park(self):
        url = reverse("park_list")
        data = {"visitor": 1, "name": "Glacier", "location": "Northern Montana", "description": "A showcase of melting glaciers, alpine meadows, carved valleys, and spectacular lakes"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        parks = Park.objects.all()
        self.assertEqual(len(parks), 2)
        self.assertEqual(Park.objects.get(id=2).name, "Glacier")

    def test_update_park(self):
        url = reverse("park_detail", args=(1,))
        data = {
            "visitor": 1,
            "name": "Yosemite",
            "location": "Middle of Nowhere CA",
            "description": "It is so pretty, just go already!",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        park = Park.objects.get(id=1)
        self.assertEqual(park.name, data["name"])
        self.assertEqual(park.visitor.id, data["visitor"])
        self.assertEqual(park.location, data["location"])
        self.assertEqual(park.description, data["description"])

    def test_delete_park(self):
        url = reverse("park_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        parks = Park.objects.all()
        self.assertEqual(len(parks), 0)
from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from resume.models import Industry
from resume.models import Position
from resume.models import PositionType

from pet_django import settings


class CreatePositionTestCase(TestCase):
    def setUp(self):
        Industry.objects.create(industry_name="First industry name")
        Industry.objects.create(industry_name="Second industry name")
        PositionType.objects.create(
            position_type_name="First type name", is_leader=False
        )

    def test_create_position(self):
        data = {"position_name": "Position name", "position_type": "First type name"}

        response = self.client.post(reverse("create_position"), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Position.objects.filter(position_name=data["position_name"]).exists()
        )
        self.assertEqual(
            {
                "position": data["position_name"],
                "industries": ["First industry name", "Second industry name"],
            },
            response.data,
        )

    def test_create_position_after_formatting(self):
        data = {"position_name": " posItion name  ", "position_type": "First type name"}

        response = self.client.post(reverse("create_position"), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Position.objects.filter(position_name="Position name").exists())
        self.assertEqual(
            {
                "position": "Position name",
                "industries": ["First industry name", "Second industry name"],
            },
            response.data,
        )

    def test_incorrect_position_name(self):
        data = {
            "position_name": "$incorrect__data",
            "position_type": "Специалист",
        }

        response = self.client.post(reverse("create_position"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"message": "Invalid data"}, response.data)

    def test_create_position_with_document_id(self):
        data = {
            "document_id": uuid4(),
            "position_name": "Position name",
            "position_type": "First type name",
        }

        response = self.client.post(reverse("create_position"), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Position.objects.filter(position_name=data["position_name"]).exists()
        )
        self.assertEqual(
            {
                "document_id": str(data["document_id"]),
                "position": data["position_name"],
                "industries": ["First industry name", "Second industry name"],
            },
            response.data,
        )

    @patch("resume.signals.send_mail")
    def test_signal_after_creating(self, mock_send_mail):
        data = {"position_name": "Position name", "position_type": "First type name"}

        self.client.post(reverse("create_position"), data=data)

        mock_send_mail.assert_called_with(
            "Новая позиция создана",
            'Была создана новая позиция с названием "Position name", '
            'которая была отнесена к виду "First type name"',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_ADMIN],
        )

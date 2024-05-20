from uuid import uuid4

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from resume.models import Industry
from resume.models import Position
from resume.models import PositionType


class CheckPositionTestCase(TestCase):
    def setUp(self):
        PositionType.objects.create(
            position_type_name="First type name", is_leader=False
        )
        PositionType.objects.create(
            position_type_name="Second type name", is_leader=True
        )

    def test_position_exists(self):
        Position.objects.create(
            position_name="Position name",
            position_type=PositionType.objects.get(
                position_type_name="First type name"
            ),
        )
        Industry.objects.create(industry_name="First industry name")
        Industry.objects.create(industry_name="Second industry name")

        response = self.client.get(
            reverse("check_position") + "?position=Position name"
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "position": "Position name",
                "industries": ["First industry name", "Second industry name"],
            },
            response.data,
        )

    def test_position_exists_with_document_id(self):
        Position.objects.create(
            position_name="Position name",
            position_type=PositionType.objects.get(
                position_type_name="First type name"
            ),
        )
        Industry.objects.create(industry_name="First industry name")
        Industry.objects.create(industry_name="Second industry name")
        document_id = uuid4()

        response = self.client.get(
            reverse("check_position")
            + f"?position=Position name&document_id={document_id}"
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "document_id": str(document_id),
                "position": "Position name",
                "industries": ["First industry name", "Second industry name"],
            },
            response.data,
        )

    def test_position_exists_after_formatting(self):
        Position.objects.create(
            position_name="Position name",
            position_type=PositionType.objects.get(
                position_type_name="First type name"
            ),
        )
        Industry.objects.create(industry_name="First industry name")
        Industry.objects.create(industry_name="Second industry name")

        response = self.client.get(
            reverse("check_position") + "?position=  pOsition name "
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "position": "Position name",
                "industries": ["First industry name", "Second industry name"],
            },
            response.data,
        )

    def test_position_does_not_exist(self):
        response = self.client.get(
            reverse("check_position") + "?position=Position name"
        )

        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            {
                "position": "Position name",
                "position_types": ["First type name", "Second type name"],
            },
            response.data,
        )

    def test_position_does_not_exist_with_document_id(self):
        document_id = uuid4()
        response = self.client.get(
            reverse("check_position")
            + f"?position=Position name&document_id={document_id}"
        )

        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            {
                "document_id": str(document_id),
                "position": "Position name",
                "position_types": ["First type name", "Second type name"],
            },
            response.data,
        )

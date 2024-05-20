from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from resume.models import General
from resume.models import Industry
from resume.models import Leader
from resume.models import Position
from resume.models import PositionType
from resume.models import Profession


class GetCompetenciesTestCase(TestCase):
    def setUp(self):
        PositionType.objects.create(
            position_type_name="First type name", is_leader=False
        )
        PositionType.objects.create(
            position_type_name="Second type name", is_leader=True
        )
        Position.objects.create(
            position_name="Standard position",
            position_type=PositionType.objects.get(
                position_type_name="First type name"
            ),
        )
        Position.objects.create(
            position_name="Leader position",
            position_type=PositionType.objects.get(
                position_type_name="Second type name"
            ),
        )
        Industry.objects.create(industry_name="Industry name")
        General.objects.create(
            general_experience="Some general experience",
            position_type=PositionType.objects.get(
                position_type_name="First type name"
            ),
        )

    @patch("resume.services.services.generate_document")
    def test_get_one_type_of_competencies(self, mock_generate_document):
        document_id = uuid4()
        mock_generate_document.return_value = str(document_id)
        position_data = {
            "position": "Standard position",
            "industry": "Industry name",
            "general_competencies": ["Some general experience"],
        }

        response = self.client.get(
            reverse("list_of_competencies")
            + "?position=Standard position&industry=Industry name"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_generate_document.assert_called_with(position_data)
        self.assertEqual(
            {
                "document_id": str(document_id),
                "positions": [
                    position_data,
                ],
            },
            response.data,
        )

    @patch("resume.services.services.generate_document")
    def test_get_competencies_when_professional_ones_exist(
        self, mock_generate_document
    ):
        Profession.objects.create(
            professional_experience="Some professional experience",
            position_type=PositionType.objects.get(
                position_type_name="First type name"
            ),
            industry=Industry.objects.get(industry_name="Industry name"),
        )
        position_data = {
            "position": "Standard position",
            "industry": "Industry name",
            "general_competencies": ["Some general experience"],
            "professional_competencies": ["Some professional experience"],
        }
        document_id = uuid4()
        mock_generate_document.return_value = str(document_id)

        response = self.client.get(
            reverse("list_of_competencies")
            + "?position=Standard position&industry=Industry name"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_generate_document.assert_called_with(position_data)
        self.assertEqual(
            {
                "document_id": str(document_id),
                "positions": [
                    position_data,
                ],
            },
            response.data,
        )

    @patch("resume.services.services.generate_document")
    def test_get_competencies_when_is_leader(self, mock_generate_document):
        General.objects.create(
            general_experience="One more general experience",
            position_type=PositionType.objects.get(
                position_type_name="Second type name"
            ),
        )
        Leader.objects.create(
            leader_experience="Some leader experience",
            position_type=PositionType.objects.get(
                position_type_name="Second type name"
            ),
        )
        position_data = {
            "position": "Leader position",
            "industry": "Industry name",
            "leader_competencies": ["Some leader experience"],
            "general_competencies": ["One more general experience"],
        }
        document_id = uuid4()
        mock_generate_document.return_value = str(document_id)

        response = self.client.get(
            reverse("list_of_competencies")
            + "?position=Leader position&industry=Industry name"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_generate_document.assert_called_with(position_data)
        self.assertEqual(
            {
                "document_id": str(document_id),
                "positions": [
                    position_data,
                ],
            },
            response.data,
        )

    @patch("resume.services.services.extend_document")
    @patch("resume.services.services.get_data_from_document")
    def test_get_competencies_with_document_id(
        self, mock_get_data_from_document, mock_extend_document
    ):
        old_document_id = str(uuid4())
        new_document_id = str(uuid4())
        mock_extend_document.return_value = new_document_id
        old_data = [
            {
                "position": "Old position name",
                "industry": "Old industry",
                "general_competencies": ["Old general experience"],
            }
        ]
        new_data = {
            "position": "Standard position",
            "industry": "Industry name",
            "general_competencies": ["Some general experience"],
        }
        mock_get_data_from_document.return_value = old_data

        response = self.client.get(
            reverse("list_of_competencies")
            + f"?position=Standard position&industry=Industry name"
            f"&document_id={old_document_id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_extend_document.assert_called_with(old_document_id, new_data)
        mock_get_data_from_document.assert_called_with(old_document_id)
        self.assertEqual(
            {"document_id": new_document_id, "positions": [old_data[0], new_data]},
            response.data,
        )

    @patch("resume.services.services.get_data_from_document")
    def test_get_competencies_duplicate(self, mock_get_data_from_document):
        old_document_id = str(uuid4())
        mock_get_data_from_document.return_value = [
            {
                "position": "Standard position",
                "industry": "Industry name",
                "general_competencies": ["Some general experience"],
            }
        ]

        response = self.client.get(
            reverse("list_of_competencies")
            + f"?position=Standard position&industry=Industry name"
            f"&document_id={old_document_id}"
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        mock_get_data_from_document.assert_called_with(old_document_id)
        self.assertEqual(
            {
                "document_id": old_document_id,
                "message": "These position and industry are already in the document",
            },
            response.data,
        )

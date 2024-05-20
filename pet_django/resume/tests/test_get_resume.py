from smtplib import SMTPDataError
from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse


class GetResumeTestCase(TestCase):
    @patch("resume.services.services.send_file_by_email.delay")
    def test_send_resume(self, mock_send_file_by_email):
        data = {"document_id": uuid4(), "email": "some_email@mail.ru"}
        mock_send_file_by_email.return_value = None

        response = self.client.post(reverse("get_resume"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "The e-mail was sent"})

    @patch("resume.services.services.send_file_by_email.delay")
    def test_send_resume_with_error(self, mock_send_file_by_email):
        data = {"document_id": uuid4(), "email": "some_email@mail.ru"}
        mock_send_file_by_email.side_effect = SMTPDataError(
            500, "Error when sending email"
        )

        response = self.client.post(reverse("get_resume"), data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, {"message": "Cannot send email"})

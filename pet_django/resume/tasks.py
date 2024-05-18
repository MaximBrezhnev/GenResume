import os

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from pet_django.settings import BASE_DIR


@shared_task
def send_file_by_email(document_id: str, email: str) -> None:
    file_path = _get_file_path(document_id)

    email_message = EmailMessage(
        "Резюме",
        "",
        settings.EMAIL_HOST_USER,
        [email],
    )

    with open(file_path, "rb") as f:
        email_message.attach("Резюме.pdf", f.read(), "application/pdf")

    email_message.send()
    os.remove(file_path)


def _get_file_path(document_id: str) -> str:
    folder_path = BASE_DIR / "resume" / "documents"
    filename = folder_path / f"{document_id}.pdf"
    return filename

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from resume.models import Position

from pet_django import settings


@receiver(post_save, sender=Position)
def send_email_to_admin(sender, instance, created, **kwargs):
    if created:
        subject = "Новая позиция создана"
        message = (
            f"Была создана новая позиция с названием: {instance.position_name}, "
            f"которая была отнесена к виду: {instance.position_type.position_type_name}"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [
            settings.EMAIL_ADMIN,
        ]

        send_mail(subject, message, from_email, recipient_list)

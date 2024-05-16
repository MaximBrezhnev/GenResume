from __future__ import absolute_import
from __future__ import unicode_literals

import os

from celery import Celery

from pet_django import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pet_django.settings")

app = Celery("pet_django")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.enable_utc = False

app.conf.update(timezone=settings.TIME_ZONE)

app.autodiscover_tasks()

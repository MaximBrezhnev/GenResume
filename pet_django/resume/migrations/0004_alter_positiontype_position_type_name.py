# Generated by Django 5.0.3 on 2024-04-05 14:53
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("resume", "0003_alter_positiontype_position_type_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="positiontype",
            name="position_type_name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
# Generated by Django 5.1 on 2024-09-04 04:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0005_manuscrito_nube_palabras"),
    ]

    operations = [
        migrations.AddField(
            model_name="paciente",
            name="usuario",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.1 on 2024-08-23 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0004_hermano_fecha_nacimiento_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="manuscrito",
            name="nube_palabras",
            field=models.ImageField(blank=True, null=True, upload_to="nubes/"),
        ),
    ]

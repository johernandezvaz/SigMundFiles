# Generated by Django 5.0.6 on 2024-07-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='extracted_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]

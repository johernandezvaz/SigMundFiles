# Generated by Django 5.0.6 on 2024-08-02 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre_usuario', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('apellidos', models.CharField(max_length=255)),
                ('cedula_profesional', models.CharField(blank=True, max_length=255, null=True)),
                ('instituto', models.CharField(max_length=255)),
                ('rol', models.CharField(choices=[('psicologo', 'Psicologo'), ('admin', 'Admin'), ('administrador del instituto', 'Administrador del Instituto')], max_length=255)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

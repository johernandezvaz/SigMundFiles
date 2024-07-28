from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, nombre_usuario, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo es requerido')
        if not nombre_usuario:
            raise ValueError('El nombre de usuario es requerido')

        email = self.normalize_email(email)
        user = self.model(nombre_usuario=nombre_usuario, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nombre_usuario, email, password, **extra_fields)

class User(AbstractBaseUser):
    nombre_usuario = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    cedula_profesional = models.CharField(max_length=255, null=True, blank=True)
    instituto = models.CharField(max_length=255)
    rol = models.CharField(max_length=255, choices=[('psicologo', 'Psicologo'), ('admin', 'Admin'), ('administrador del instituto', 'Administrador del Instituto')])
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellidos', 'instituto', 'rol']

    def __str__(self):
        return self.nombre_usuario
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo es requerido')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
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
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'instituto', 'rol']
    
    def __str__(self):
        return self.email

# Modelos para Pacientes y Citas


class Paciente(models.Model):
    foto = models.ImageField(upload_to='fotos_pacientes/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nombre_completo = models.CharField(max_length=255, blank=True, null=True, default='Nombre Desconocido')
    edad = models.IntegerField(blank=True, null=True, default=0)
    genero = models.CharField(max_length=10, blank=True, null=True, default='otro', choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')])
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=255, blank=True, null=True)
    escolaridad = models.CharField(max_length=255, blank=True, null=True)
    estado_civil = models.CharField(max_length=50, blank=True, null=True, default='soltero', choices=[('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado'), ('viudo', 'Viudo')])
    correo = models.EmailField(blank=True, null=True, default='default@example.com')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    acude_voluntariamente = models.BooleanField(default=True)

    # Información de los padres
    nombre_padre = models.CharField(max_length=255, blank=True, null=True)
    edad_padre = models.IntegerField(blank=True, null=True, default=0)
    escolaridad_padre = models.CharField(max_length=255, blank=True, null=True)
    ocupacion_padre = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_patologicos_padre = models.TextField(blank=True, null=True)

    nombre_madre = models.CharField(max_length=255, blank=True, null=True)
    edad_madre = models.IntegerField(blank=True, null=True, default=0)
    escolaridad_madre = models.CharField(max_length=255, blank=True, null=True)
    ocupacion_madre = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_patologicos_madre = models.TextField(blank=True, null=True)

    estado_civil_padres = models.CharField(max_length=50, blank=True, null=True, default='soltero', choices=[('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado'), ('viudo', 'Viudo')])

    # Información de los hermanos (hasta 3, no obligatorios)
    nombre_hermano_1 = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_hermano_1 = models.TextField(blank=True, null=True)
    edad_hermano_1 = models.IntegerField(blank=True, null=True, default=0)
    grado_escolar_hermano_1 = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_patologicos_hermano_1 = models.TextField(blank=True, null=True)
    adicciones_hermano_1 = models.TextField(blank=True, null=True)

    nombre_hermano_2 = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_hermano_2 = models.TextField(blank=True, null=True)
    edad_hermano_2 = models.IntegerField(blank=True, null=True, default=0)
    grado_escolar_hermano_2 = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_patologicos_hermano_2 = models.TextField(blank=True, null=True)
    adicciones_hermano_2 = models.TextField(blank=True, null=True)

    nombre_hermano_3 = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_hermano_3 = models.TextField(blank=True, null=True)
    edad_hermano_3 = models.IntegerField(blank=True, null=True, default=0)
    grado_escolar_hermano_3 = models.CharField(max_length=255, blank=True, null=True)
    antecedentes_patologicos_hermano_3 = models.TextField(blank=True, null=True)
    adicciones_hermano_3 = models.TextField(blank=True, null=True)

    # Otras personas que viven en el hogar
    otras_personas_hogar = models.TextField(blank=True, null=True)

    # Preguntas de salud con opciones (Nunca, Pasado, Presente)
    asma_alergias = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    catarros_frecuentes = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    epilepsia_convulsiones = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    convulsiones_febriles = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    manias = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    lesiones_cabeza = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    cirugias_hospitalizacion = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    problemas_vision = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')
    problemas_apetito = models.CharField(max_length=10, choices=[('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')], blank=True, null=True, default='nunca')

    def save(self, *args, **kwargs):
        if self.fecha_nacimiento:
            today = date.today()
            self.edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        super(Paciente, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_completo or "Paciente Desconocido"


class Cita(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

    def __str__(self):
        return f'{self.fecha} con {self.paciente.nombre}'


class Manuscrito(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='manuscritos/')
    texto = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

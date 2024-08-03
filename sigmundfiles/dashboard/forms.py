from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Cita, Paciente

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nombre_usuario', 'email', 'nombre', 'apellidos', 'cedula_profesional', 'instituto', 'rol', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion']
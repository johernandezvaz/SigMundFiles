from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Cita, Paciente, Manuscrito

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'nombre', 'apellidos', 'cedula_profesional', 'instituto', 'rol']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha']

from django import forms
from .models import Paciente
import datetime

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'foto',
            'nombre_completo',
            'edad',
            'genero',
            'fecha_nacimiento',
            'lugar_nacimiento',
            'escolaridad',
            'estado_civil',
            'correo',
            'telefono',
            'direccion',
            'religion',
            'acude_voluntariamente',
            'nombre_padre',
            'edad_padre',
            'escolaridad_padre',
            'ocupacion_padre',
            'antecedentes_patologicos_padre',
            'nombre_madre',
            'edad_madre',
            'escolaridad_madre',
            'ocupacion_madre',
            'antecedentes_patologicos_madre',
            'estado_civil_padres',
            'nombre_hermano_1',
            'antecedentes_hermano_1',
            'edad_hermano_1',
            'grado_escolar_hermano_1',
            'antecedentes_patologicos_hermano_1',
            'adicciones_hermano_1',
            'nombre_hermano_2',
            'antecedentes_hermano_2',
            'edad_hermano_2',
            'grado_escolar_hermano_2',
            'antecedentes_patologicos_hermano_2',
            'adicciones_hermano_2',
            'nombre_hermano_3',
            'antecedentes_hermano_3',
            'edad_hermano_3',
            'grado_escolar_hermano_3',
            'antecedentes_patologicos_hermano_3',
            'adicciones_hermano_3',
            'otras_personas_hogar',
            'asma_alergias',
            'catarros_frecuentes',
            'epilepsia_convulsiones',
            'convulsiones_febriles',
            'manias',
            'lesiones_cabeza',
            'cirugias_hospitalizacion',
            'problemas_vision',
            'problemas_apetito',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'value': datetime.date.today()}),
        }

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        
        # Deshabilitar el campo edad
        self.fields['edad'].disabled = True
        
        # Personalización de campos que no son obligatorios
        self.fields['nombre_hermano_1'].required = False
        self.fields['antecedentes_hermano_1'].required = False
        self.fields['edad_hermano_1'].required = False
        self.fields['grado_escolar_hermano_1'].required = False
        self.fields['antecedentes_patologicos_hermano_1'].required = False
        self.fields['adicciones_hermano_1'].required = False

        self.fields['nombre_hermano_2'].required = False
        self.fields['antecedentes_hermano_2'].required = False
        self.fields['edad_hermano_2'].required = False
        self.fields['grado_escolar_hermano_2'].required = False
        self.fields['antecedentes_patologicos_hermano_2'].required = False
        self.fields['adicciones_hermano_2'].required = False

        self.fields['nombre_hermano_3'].required = False
        self.fields['antecedentes_hermano_3'].required = False
        self.fields['edad_hermano_3'].required = False
        self.fields['grado_escolar_hermano_3'].required = False
        self.fields['antecedentes_patologicos_hermano_3'].required = False
        self.fields['adicciones_hermano_3'].required = False

        # Campos adicionales para customizaciones
        self.fields['foto'].widget = forms.ClearableFileInput()
        self.fields['acude_voluntariamente'].widget = forms.CheckboxInput()

        # Opciones de las preguntas de salud
        opciones_salud = [('nunca', 'Nunca'), ('pasado', 'Pasado'), ('presente', 'Presente')]
        self.fields['asma_alergias'].widget = forms.Select(choices=opciones_salud)
        self.fields['catarros_frecuentes'].widget = forms.Select(choices=opciones_salud)
        self.fields['epilepsia_convulsiones'].widget = forms.Select(choices=opciones_salud)
        self.fields['convulsiones_febriles'].widget = forms.Select(choices=opciones_salud)
        self.fields['manias'].widget = forms.Select(choices=opciones_salud)
        self.fields['lesiones_cabeza'].widget = forms.Select(choices=opciones_salud)
        self.fields['cirugias_hospitalizacion'].widget = forms.Select(choices=opciones_salud)
        self.fields['problemas_vision'].widget = forms.Select(choices=opciones_salud)
        self.fields['problemas_apetito'].widget = forms.Select(choices=opciones_salud)

        # Configurar todos los campos de fecha con calendario y fecha predeterminada actual
        for field_name in self.fields:
            if isinstance(self.fields[field_name].widget, forms.DateInput):
                self.fields[field_name].widget.attrs['value'] = datetime.date.today().strftime('%Y-%m-%d')
                self.fields[field_name].widget.attrs['type'] = 'date'


# Nuevo formulario para manuscritos
class ManuscritoForm(forms.ModelForm):
    class Meta:
        model = Manuscrito
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        super(ManuscritoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget = forms.ClearableFileInput()

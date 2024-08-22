from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Hogar, User, Cita, Paciente, Manuscrito, Padres, Hermano, Salud
from django.utils.translation import gettext_lazy as _





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
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "El correo electrónico o la contraseña son incorrectos.",
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha']

# Nuevo formulario para manuscritos
class ManuscritoForm(forms.ModelForm):
    class Meta:
        model = Manuscrito
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        super(ManuscritoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget = forms.ClearableFileInput()

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'foto', 'nombre_completo', 'fecha_nacimiento', 'edad', 'genero', 'lugar_nacimiento', 
            'escolaridad', 'estado_civil', 'correo', 'telefono', 'direccion', 'religion', 'acude_voluntariamente'
        ]
        widgets = {
            'edad': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class PadresForm(forms.ModelForm):
    class Meta:
        model = Padres
        fields = [
            'nombre_padre', 'fecha_nacimiento_padre', 'edad_padre', 'escolaridad_padre', 'ocupacion_padre', 'antecedentes_patologicos_padre',
            'nombre_madre', 'fecha_nacimiento_madre', 'edad_madre', 'escolaridad_madre', 'ocupacion_madre', 'antecedentes_patologicos_madre',
            'estado_civil_padres'
        ]
        widgets = {
            'edad_padre': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'edad_madre': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'fecha_nacimiento_padre': forms.DateInput(attrs={'type': 'date'}),
            'fecha_nacimiento_madre': forms.DateInput(attrs={'type': 'date'}),
        }

PadresFormSet = forms.modelformset_factory(
    Padres,
    form=PadresForm,
    extra=2,  # Puedes configurar cuántos formularios adicionales mostrar
    can_delete=True,
)

# Formset para hermanos
HermanoFormSet = forms.inlineformset_factory(
    Paciente, Hermano, 
    fields=['nombre', 'fecha_nacimiento', 'edad', 'grado_escolar', 'antecedentes', 'antecedentes_patologicos', 'adicciones'],
    extra=1,  # Número de formularios adicionales a mostrar
    can_delete=True,
    widgets={
        'edad': forms.NumberInput(attrs={'readonly': 'readonly'}),
        'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
    }
)

# Formset para salud
SaludFormSet = forms.inlineformset_factory(
    Paciente, Salud,
    fields=[
        'asma_alergias', 'catarros_frecuentes', 'epilepsia_convulsiones', 'convulsiones_febriles', 'manias',
        'lesiones_cabeza', 'cirugias_hospitalizacion', 'problemas_vision', 'problemas_apetito'
    ],
    extra=1,  # Número de formularios adicionales a mostrar
    can_delete=True  # Permitir eliminar instancias
)

class HogarForm(forms.ModelForm):
    class Meta:
        model = Hogar
        fields = ['otras_personas']

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm, CitaForm, ManuscritoForm, PacienteForm, PadresForm, HermanoFormSet, SaludFormSet, HogarForm
from django.contrib.auth.decorators import login_required
from .models import Paciente, Cita, Manuscrito
import pytesseract
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def auth_view(request):
    print("Vista auth_view ejecutada")
    login_form = UserLoginForm(auto_id='login_%s')
    registration_form = UserRegistrationForm(auto_id='register_%s')

    if request.method == 'POST':
        print("Método POST detectado")
        print("Contenido de request.POST:", request.POST)
        if 'login' in request.POST:
            login_form = UserLoginForm(data=request.POST, auto_id='login_%s')
            if login_form.is_valid():
                print("Formulario de login es válido")
                user = login_form.get_user()
                if user is not None:
                    login(request, user)
                    print("Usuario autenticado y logueado:", user)
                    return redirect('dashboard')
                else:
                    print("No se pudo autenticar al usuario")
            else:
                print("Formulario de login no es válido:", login_form.errors)
        elif 'register' in request.POST:
            print("Formulario de registro enviado")
            print("Contenido de request.POST:", request.POST)

            registration_form = UserRegistrationForm(request.POST, auto_id='register_%s')
            if registration_form.is_valid():
                registration_form.save()
                print("Registro exitoso, redirigiendo a login")
                return redirect('login')
            else:
                print("Formulario de registro no es válido:", registration_form.errors)

    context = {
        'login_form': login_form,
        'registration_form': registration_form,
    }

    return render(request, 'dashboard/login.html', context)



def home(request):
    return render(request, 'dashboard/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    # Obtener el término de búsqueda desde el input del usuario
    search_query = request.GET.get('search', '')

    if search_query:
        # Filtrar pacientes que coincidan con el nombre o apellidos
        pacientes = Paciente.objects.filter(
            Q(nombre_completo__icontains=search_query) 
        )
    else:
        # Si no hay término de búsqueda, obtener todos los pacientes
        pacientes = Paciente.objects.all()

    # Verificar si la solicitud es AJAX (para respuestas en tiempo real)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Preparar datos de pacientes en formato JSON
        pacientes_data = [
            {
                'id': paciente.id,
                'nombre_completo': f"{paciente.nombre} {paciente.apellidos}",
                'edad': paciente.edad,
                'foto': paciente.foto.url if paciente.foto else None,
            }
            for paciente in pacientes
        ]
        # Devolver los datos como JSON
        return JsonResponse({'pacientes': pacientes_data})
    
    # Para solicitudes no AJAX, renderizar la página normalmente
    context = {
        'pacientes': pacientes,
    }
    return render(request, 'dashboard/dashboard.html', context)




@login_required
def agregar_cita_view(request):
    user = request.user
    pacientes = Paciente.objects.filter(usuario=user)

    if  pacientes:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.usuario = user
            cita.save()
            return redirect('dashboard')
    else:
        form = CitaForm()

    return render(request, 'dashboard/agregar_cita.html', {'form': form, 'pacientes': pacientes})

@login_required
def agregar_paciente_view(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, request.FILES)
        padres_form = PadresForm(request.POST, request.FILES)
        hermano_formset = HermanoFormSet(request.POST, prefix='hermanos')
        salud_formset = SaludFormSet(request.POST, prefix='salud')
        hogar_form = HogarForm(request.POST)

        if paciente_form.is_valid() and hermano_formset.is_valid() and salud_formset.is_valid() and hogar_form.is_valid():
            # Guardar el paciente
            paciente = paciente_form.save()

            # Guardar los datos de los padres si el formulario es válido
            if padres_form.is_valid():
                padres = padres_form.save(commit=False)
                padres.paciente = paciente
                padres.save()

            # Guardar los datos de los hermanos
            hermanos = hermano_formset.save(commit=False)
            for hermano in hermanos:
                hermano.paciente = paciente
                hermano.save()

            # Guardar los datos de salud
            salud = salud_formset.save(commit=False)
            for s in salud:
                s.paciente = paciente
                s.save()

            # Guardar los datos del hogar
            hogar = hogar_form.save(commit=False)
            hogar.paciente = paciente
            hogar.save()

            return redirect('dashboard')  # Redirige a una página de éxito o al dashboard
    else:
        paciente_form = PacienteForm()
        padres_form = PadresForm()
        hermano_formset = HermanoFormSet(prefix='hermanos')
        salud_formset = SaludFormSet(prefix='salud')
        hogar_form = HogarForm()

    return render(request, 'dashboard/add_paciente.html', {
        'paciente_form': paciente_form,
        'padres_form': padres_form,
        'hermano_formset': hermano_formset,
        'salud_formset': salud_formset,
        'hogar_form': hogar_form,
    })

def generar_nube_de_palabras(texto):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('media/wordclouds/nube_de_palabras.png')
    plt.close()

@login_required
def agregar_nota_view(request, paciente_id):
    if request.method == 'POST':
        nueva_nota = request.POST.get('nueva_nota')
        if nueva_nota:
            cita = Cita.objects.create(
                paciente_id=paciente_id,
                texto=nueva_nota,
                usuario=request.user
            )
            cita.save()
            return redirect('detalle_paciente', paciente_id=paciente_id)
    return redirect('detalle_paciente', paciente_id=paciente_id)

@login_required
def generar_nube_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    citas = Cita.objects.filter(paciente=paciente)
    
    # Combina todos los textos de las citas en un solo string
    texto_completo = ' '.join([cita.texto for cita in citas])
    
    # Generar la nube de palabras
    generar_nube_de_palabras(texto_completo)
    
    return redirect('detalle_paciente', paciente_id=paciente_id)

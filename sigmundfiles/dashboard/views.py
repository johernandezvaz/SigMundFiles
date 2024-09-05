import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
import torch
from torchvision import transforms
from django.contrib.auth import login, authenticate, logout
from django.core.files.storage import default_storage
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, CitaForm, ManuscritoForm, PacienteForm, PadresForm, HermanoFormSet, SaludFormSet, HogarForm
from django.contrib.auth.decorators import login_required
from .models import Paciente, Cita, Manuscrito
from django.views.decorators.csrf import csrf_exempt
import cv2
import easyocr
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from google.cloud import vision
from django.core.files.storage import default_storage
import torch.nn as nn
import pytesseract  


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

    # Filtrar pacientes por el usuario actual
    pacientes = Paciente.objects.filter(usuario=request.user)

    if search_query:
        # Si hay un término de búsqueda, filtrar los pacientes que coincidan con el nombre completo
        pacientes = pacientes.filter(Q(nombre_completo__icontains=search_query))

    # Verificar si la solicitud es AJAX (para respuestas en tiempo real)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Preparar datos de pacientes en formato JSON
        pacientes_data = [
            {
                'id': paciente.id,
                'nombre_completo': f"{paciente.nombre_completo}",
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


def gestionar_manuscritos(request, paciente_id):
    # Obtener el paciente
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Obtener los manuscritos asociados a ese paciente
    manuscritos = Manuscrito.objects.filter(paciente=paciente)
    print(manuscritos)  # Debugging

    # Renderizar el template con la información de manuscritos
    return render(request, 'gestionar_manuscritos.html', {'paciente': paciente, 'manuscritos': manuscritos})



def borrar_manuscrito(request, manuscrito_id, paciente_id):
    # Obtener el manuscrito específico y verificar que pertenezca al paciente correcto
    manuscrito = get_object_or_404(Manuscrito, id=manuscrito_id, paciente_id=paciente_id)

    # Eliminar el manuscrito
    manuscrito.delete()

    # Redirigir de nuevo al dashboard (ajusta según tu vista)
    return redirect('dashboard')  # Redirige al nombre de la vista asociada a tu dashboard



# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

@login_required
def agregar_nota_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        fecha = request.POST.get('fecha')
        texto_extraido = ""

        if imagen:
            # Guardar temporalmente la imagen para procesarla
            temp_image_path = default_storage.save('temp_image.jpg', imagen)
            temp_image_full_path = default_storage.path(temp_image_path)

            # Preprocesamiento de la imagen
            pil_image = Image.open(temp_image_full_path)
            open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY, 31, 2)

            # Usar Tesseract para leer el texto
            texto_extraido = pytesseract.image_to_string(thresh_image, lang='spa')

            # Eliminar la imagen temporal después de extraer el texto
            default_storage.delete(temp_image_path)
        
        # Renderizar la página con el texto extraído en el popup
        return render(request, 'analisis_citas_template.html', {
            'paciente': paciente,
            'texto_extraido': texto_extraido,
            'fecha': fecha,
            'mostrar_popup': True  # Indicador para desplegar el popup
        })

    return render(request, 'analisis_citas_template.html', {'paciente': paciente})



@csrf_exempt
def procesar_imagen_ocr(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        imagen = request.FILES['imagen']

        # Guardar la imagen temporalmente
        temp_image_path = default_storage.save('temp_image.jpg', imagen)
        temp_image_full_path = default_storage.path(temp_image_path)

        try:
            # Preprocesar la imagen
            image = cv2.imread(temp_image_full_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            denoised_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
            thresh_image = cv2.adaptiveThreshold(
                denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )

            # Extraer texto con Tesseract
            texto_extraido = pytesseract.image_to_string(thresh_image, lang='spa')

            # Eliminar la imagen temporal después de extraer el texto
            default_storage.delete(temp_image_path)

            # Guardar el texto extraído en el modelo Manuscrito
            paciente_id = request.POST.get('paciente_id')
            fecha_cita = request.POST.get('fecha')
            paciente = Paciente.objects.get(id=paciente_id)
            manuscrito = Manuscrito(paciente=paciente, imagen=imagen, texto=texto_extraido)
            manuscrito.save()

            # Generar la nube de palabras (suponiendo que ya tienes la función implementada)
            nube_path = generar_nube_de_palabras(texto_extraido, paciente_id, fecha_cita)
            manuscrito.nube_palabras = nube_path
            manuscrito.save()

            return JsonResponse({'texto': texto_extraido, 'nube_url': f'/{nube_path}'})

        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return JsonResponse({'error': 'Ocurrió un error al procesar la imagen'}, status=500)

    return JsonResponse({'error': 'No se envió ninguna imagen'}, status=400)


def generar_nube_de_palabras(texto, paciente_id, fecha_cita):
    # Crear la ruta de la carpeta para las nubes de palabras del paciente
    paciente_folder = os.path.join('media/wordclouds', f'paciente_{paciente_id}')
    if not os.path.exists(paciente_folder):
        os.makedirs(paciente_folder)
    
    # Nombre de la imagen basado en la fecha de la cita
    nombre_imagen = f'nube_{fecha_cita}.png'
    ruta_imagen = os.path.join(paciente_folder, nombre_imagen)
    
    # Generar la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    
    # Guardar la imagen
    wordcloud.to_file(ruta_imagen)
    
    print(f"Nube de palabras generada en: {ruta_imagen}")
    
    return ruta_imagen




def generar_nube_de_palabras(texto, paciente_id, fecha_cita):
    # Crear la ruta de la carpeta para las nubes de palabras del paciente
    paciente_folder = os.path.join('media/wordclouds', f'paciente_{paciente_id}')
    if not os.path.exists(paciente_folder):
        os.makedirs(paciente_folder)
    
    # Nombre de la imagen basado en la fecha de la cita
    nombre_imagen = f'nube_{fecha_cita}.png'
    ruta_imagen = os.path.join(paciente_folder, nombre_imagen)
    
    # Generar la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    
    # Guardar la imagen
    wordcloud.to_file(ruta_imagen)
    
    print(f"Nube de palabras generada en: {ruta_imagen}")
    
    return ruta_imagen



@login_required
def generar_nube_popup_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == "POST":
        texto = request.POST.get('texto')
        
        if texto:
            # Generar la nube de palabras y obtener la URL
            nube_path = generar_nube_de_palabras(texto)
            
            # Asegúrate de que la URL refleje la ubicación correcta
            nube_url = f'/{nube_path}'
            return redirect('dashboard') 

    return JsonResponse({'error': 'No se pudo generar la nube de palabras.'})   
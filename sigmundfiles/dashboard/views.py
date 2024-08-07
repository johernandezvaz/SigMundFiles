from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm, CitaForm, PacienteForm
from django.contrib.auth.decorators import login_required
from .models import Paciente, Cita

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'dashboard/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard después de iniciar sesión
    else:
        form = UserLoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def home(request):
    return render(request, 'dashboard/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    pacientes = Paciente.objects.filter(usuario=user)
    citas = Cita.objects.filter(usuario=user)

    context = {
        'pacientes': pacientes,
        'citas': citas,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def agregar_cita_view(request):
    user = request.user
    pacientes = Paciente.objects.filter(usuario=user)

    if not pacientes:
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
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.usuario = request.user
            paciente.save()
            return redirect('dashboard')
    else:
        form = PacienteForm()
    return render(request, 'dashboard/add_paciente.html', {'form': form})
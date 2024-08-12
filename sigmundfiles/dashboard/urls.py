from django.urls import path
from .views import (
    register, login_view, home, logout_view, dashboard_view, 
    agregar_cita_view, agregar_paciente_view, 
    procesar_manuscrito
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/agregar-cita/', agregar_cita_view, name='agregar_cita'),
    path('dashboard/agregar-paciente/', agregar_paciente_view, name='agregar_paciente'),
    path('dashboard/procesar-manuscrito/', procesar_manuscrito, name='procesar_manuscrito'),
]

from django.urls import path
from .views import (
    agregar_nota_view, auth_view, generar_nube_view, home, logout_view, dashboard_view, 
    agregar_cita_view, agregar_paciente_view, 
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/agregar-paciente/', agregar_paciente_view, name='agregar_paciente'),
    path('agregar_nota/<int:paciente_id>/', agregar_nota_view, name='agregar_nota'),
    path('generar_nube/<int:paciente_id>/', generar_nube_view, name='generar_nube'),
]

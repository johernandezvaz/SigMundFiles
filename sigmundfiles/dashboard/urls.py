from django.urls import path
from .views import (
    agregar_nota_view, auth_view, generar_nube_view, home, logout_view, dashboard_view, 
    agregar_cita_view, agregar_paciente_view, procesar_imagen_ocr, 
)
from dashboard import views

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/agregar-paciente/', agregar_paciente_view, name='agregar_paciente'),
    path('agregar_nota/<int:paciente_id>/', agregar_nota_view, name='agregar_nota'),
    path('generar_nube/<int:paciente_id>/', generar_nube_view, name='generar_nube'),
    path('procesar-imagen-ocr/', procesar_imagen_ocr, name='procesar_imagen_ocr'),
    path('paciente/<int:paciente_id>/manuscritos/', views.gestionar_manuscritos, name='gestionar_manuscritos'),
    path('borrar-manuscrito/<int:manuscrito_id>/', views.borrar_manuscrito, name='borrar_manuscrito'),

]

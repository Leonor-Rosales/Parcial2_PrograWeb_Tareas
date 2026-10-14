from django.urls import path
from tareas import views

urlpatterns = [
    path('', views.dashboard),
    path('api/tarea/', views.listar),
    path('api/tarea/<int:id>', views.detalle),
]

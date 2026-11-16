from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo_publico, name='catalogo_publico'),
    path('experiencia/<int:experiencia_id>/', views.detalle_experiencia, name='detalle_experiencia'),
]

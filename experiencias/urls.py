from django.urls import path
from . import views

urlpatterns = [
    # Paneles principales
    path('panel/admin/', views.panel_admin, name='panel_admin'),
    path('panel/guia/', views.panel_guia, name='panel_guia'),
    path('panel/turista/', views.panel_turista, name='panel_turista'),

    # CRUD Categorías (Solo Admin)
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # CRUD Experiencias (Admin y Guía)
    path('lista/', views.lista_experiencias, name='lista_experiencias'),
    path('crear/', views.crear_experiencia, name='crear_experiencia'),
    path('editar/<int:experiencia_id>/', views.editar_experiencia, name='editar_experiencia'),
    path('eliminar/<int:experiencia_id>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    path('grupo/<int:experiencia_id>/', views.detalle_grupo_experiencia, name='detalle_grupo_experiencia'),

    # Reservas y Pagos
    path('reservar/<int:experiencia_id>/', views.reservar_experiencia, name='reservar_experiencia'),
    path('pagar/<int:inscripcion_id>/', views.confirmar_pago, name='confirmar_pago'),
    path('cancelar/<int:inscripcion_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/todas/', views.todas_las_reservas, name='todas_las_reservas'),
]

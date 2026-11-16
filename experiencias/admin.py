from django.contrib import admin
from django.contrib import admin
from .models import Categoria, Experiencia, Inscripcion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'precio', 'cupo_maximo', 'fecha_hora', 'creador', 'activo')
    list_filter = ('activo', 'categoria', 'creador')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_hora'

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('turista', 'experiencia', 'fecha_inscripcion', 'estado_pago')
    list_filter = ('estado_pago', 'fecha_inscripcion')
    search_fields = ('turista__username', 'experiencia__titulo')

# Register your models here.

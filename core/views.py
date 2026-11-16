from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from experiencias.models import Experiencia, Categoria

def inicio(request):
    # Mostramos las 3 experiencias activas y futuras más próximas como destacadas
    experiencias_destacadas = Experiencia.objects.filter(
        activo=True,
        categoria__activo=True,
        fecha_hora__gte=timezone.now()
    ).order_by('fecha_hora')[:3]

    context = {
        'experiencias_destacadas': experiencias_destacadas
    }
    return render(request, 'core/inicio.html', context)


def catalogo_publico(request):
    categorias = Categoria.objects.filter(activo=True)
    experiencias = Experiencia.objects.filter(
        activo=True,
        categoria__activo=True
    ).order_by('fecha_hora')

    # Filtro opcional por categoría desde la URL (ej: /catalogo/?categoria=1)
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        experiencias = experiencias.filter(categoria_id=categoria_id)

    context = {
        'experiencias': experiencias,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id
    }
    return render(request, 'core/catalogo.html', context)


def detalle_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(Experiencia, id=experiencia_id, activo=True)
    inscritos = experiencia.inscripciones.count()
    cupos_disponibles = experiencia.cupo_maximo - inscritos

    context = {
        'experiencia': experiencia,
        'cupos_disponibles': cupos_disponibles
    }
    return render(request, 'core/detalle_experiencia.html', context)

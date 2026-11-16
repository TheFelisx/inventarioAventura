from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Categoria, Experiencia, Inscripcion
from .forms import CategoriaForm, ExperienciaForm

# Funciones auxiliares de roles
def get_rol(user):
    return user.perfil.rol if hasattr(user, 'perfil') else None


# ==========================================
# PANELES PRINCIPALES POR ROL
# ==========================================

@login_required
def panel_admin(request):
    if get_rol(request.user) != 'ADMIN':
        return redirect('redireccion_rol')

    context = {
        'total_usuarios': User.objects.filter(is_superuser=False).count(),
        'total_categorias': Categoria.objects.count(),
        'total_experiencias': Experiencia.objects.count(),
        'total_reservas': Inscripcion.objects.count(),
        'ingresos': Inscripcion.objects.filter(estado_pago='CONFIRMADO').aggregate(t=Sum('experiencia__precio'))['t'] or 0,
        'ultimas_reservas': Inscripcion.objects.select_related('turista', 'experiencia').order_by('-fecha_inscripcion')[:10]
    }
    return render(request, 'experiencias/panel_admin.html', context)


@login_required
def panel_guia(request):
    if get_rol(request.user) != 'GUIA':
        return redirect('redireccion_rol')

    # Regla de la guía: El Guía solo ve sus propias experiencias
    mis_experiencias = Experiencia.objects.filter(creador=request.user).order_by('fecha_hora')
    return render(request, 'experiencias/panel_guia.html', {'experiencias': mis_experiencias})


@login_required
def panel_turista(request):
    if get_rol(request.user) != 'TURISTA':
        return redirect('redireccion_rol')

    mis_reservas = Inscripcion.objects.filter(turista=request.user).select_related('experiencia').order_by('-fecha_inscripcion')
    return render(request, 'experiencias/panel_turista.html', {'reservas': mis_reservas})


# ==========================================
# CRUD DE CATEGORÍAS (SOLO ADMINISTRADOR)
# ==========================================

@login_required
def lista_categorias(request):
    if get_rol(request.user) != 'ADMIN':
        messages.error(request, "Acceso denegado. Solo los administradores gestionan categorías.")
        return redirect('redireccion_rol')

    categorias = Categoria.objects.all()
    return render(request, 'experiencias/lista_categorias.html', {'categorias': categorias})


@login_required
def crear_categoria(request):
    if get_rol(request.user) != 'ADMIN':
        return redirect('redireccion_rol')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'experiencias/form_categoria.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_categoria(request, categoria_id):
    if get_rol(request.user) != 'ADMIN':
        return redirect('redireccion_rol')

    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada.")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'experiencias/form_categoria.html', {'form': form, 'accion': 'Editar'})


@login_required
def eliminar_categoria(request, categoria_id):
    if get_rol(request.user) != 'ADMIN':
        return redirect('redireccion_rol')

    categoria = get_object_or_404(Categoria, id=categoria_id)
    try:
        categoria.delete()
        messages.success(request, "Categoría eliminada.")
    except Exception:
        messages.error(request, "No se puede eliminar esta categoría porque tiene experiencias asociadas.")
    return redirect('lista_categorias')


# ==========================================
# CRUD DE EXPERIENCIAS (ADMIN Y GUÍA)
# ==========================================

@login_required
def lista_experiencias(request):
    rol = get_rol(request.user)
    if rol == 'ADMIN':
        # Admin ve todas las experiencias del sistema
        experiencias = Experiencia.objects.select_related('categoria', 'creador').all()
    elif rol == 'GUIA':
        # Guía solo ve las experiencias creadas por él mismo
        experiencias = Experiencia.objects.filter(creador=request.user).select_related('categoria')
    else:
        return redirect('catalogo_publico')

    return render(request, 'experiencias/lista_experiencias.html', {'experiencias': experiencias})


@login_required
def crear_experiencia(request):
    rol = get_rol(request.user)
    if rol not in ['ADMIN', 'GUIA']:
        return redirect('redireccion_rol')

    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.creador = request.user # Asigna automáticamente al usuario logueado
            experiencia.save()
            messages.success(request, "Experiencia registrada con éxito.")
            return redirect('lista_experiencias')
    else:
        form = ExperienciaForm()
    return render(request, 'experiencias/form_experiencia.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_experiencia(request, experiencia_id):
    rol = get_rol(request.user)
    if rol == 'ADMIN':
        experiencia = get_object_or_404(Experiencia, id=experiencia_id)
    elif rol == 'GUIA':
        # Guía solo puede editar si él es el creador
        experiencia = get_object_or_404(Experiencia, id=experiencia_id, creador=request.user)
    else:
        return redirect('redireccion_rol')

    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Experiencia actualizada.")
            return redirect('lista_experiencias')
    else:
        form = ExperienciaForm(instance=experiencia)
    return render(request, 'experiencias/form_experiencia.html', {'form': form, 'accion': 'Editar'})


@login_required
def eliminar_experiencia(request, experiencia_id):
    # Regla de la guía: SOLO el Administrador puede eliminar experiencias
    if get_rol(request.user) != 'ADMIN':
        messages.error(request, "Solo un Administrador puede eliminar experiencias.")
        return redirect('lista_experiencias')

    experiencia = get_object_or_404(Experiencia, id=experiencia_id)
    experiencia.delete()
    messages.success(request, "Experiencia eliminada del sistema.")
    return redirect('lista_experiencias')


@login_required
def detalle_grupo_experiencia(request, experiencia_id):
    rol = get_rol(request.user)
    if rol == 'ADMIN':
        experiencia = get_object_or_404(Experiencia, id=experiencia_id)
    elif rol == 'GUIA':
        experiencia = get_object_or_404(Experiencia, id=experiencia_id, creador=request.user)
    else:
        return redirect('redireccion_rol')

    inscritos = experiencia.inscripciones.select_related('turista').all()
    return render(request, 'experiencias/detalle_grupo.html', {'experiencia': experiencia, 'inscritos': inscritos})


# ==========================================
# RESERVAS Y PAGOS (TURISTA Y REPORTE ADMIN)
# ==========================================

@login_required
def reservar_experiencia(request, experiencia_id):
    if get_rol(request.user) != 'TURISTA':
        messages.error(request, "Solo los usuarios con rol Turista pueden realizar reservas.")
        return redirect('redireccion_rol')

    experiencia = get_object_or_404(Experiencia, id=experiencia_id, activo=True)

    # Validar cupos disponibles
    if experiencia.inscripciones.count() >= experiencia.cupo_maximo:
        messages.error(request, "Lo sentimos, no quedan cupos disponibles para esta actividad.")
        return redirect('catalogo_publico')

    try:
        inscripcion = Inscripcion(turista=request.user, experiencia=experiencia)
        inscripcion.save() # Dispara automáticamente la validación de choque de horario
        messages.success(request, f"¡Reserva registrada para '{experiencia.titulo}'! Estado: Pendiente de pago.")
    except ValidationError as e:
        for error in e.messages:
            messages.error(request, error)

    return redirect('panel_turista')


@login_required
def confirmar_pago(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, turista=request.user)
    inscripcion.estado_pago = 'CONFIRMADO'
    inscripcion.save()
    messages.success(request, f"Pago confirmado para '{inscripcion.experiencia.titulo}'.")
    return redirect('panel_turista')


@login_required
def cancelar_reserva(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, turista=request.user)
    titulo = inscripcion.experiencia.titulo
    inscripcion.delete()
    messages.success(request, f"Has cancelado tu reserva para '{titulo}'.")
    return redirect('panel_turista')


@login_required
def todas_las_reservas(request):
    if get_rol(request.user) != 'ADMIN':
        return redirect('redireccion_rol')

    reservas = Inscripcion.objects.select_related('turista', 'experiencia').all().order_by('-fecha_inscripcion')
    return render(request, 'experiencias/todas_reservas.html', {'reservas': reservas})

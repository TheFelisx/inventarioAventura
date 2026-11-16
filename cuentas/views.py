from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroTuristaForm, AdminCrearUsuarioForm, AdminEditarUsuarioForm

# Función auxiliar para verificar si el usuario es ADMIN
def es_admin(user):
    return hasattr(user, 'perfil') and user.perfil.rol == 'ADMIN'


# 1. Registro público de Turistas
def registro_turista(request):
    if request.user.is_authenticated:
        return redirect('redireccion_rol')

    if request.method == 'POST':
        form = RegistroTuristaForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.perfil.telefono = form.cleaned_data.get('telefono')
            user.perfil.rol = 'TURISTA'
            user.perfil.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido/a {user.first_name}! Tu cuenta de Turista fue creada.")
            return redirect('redireccion_rol')
    else:
        form = RegistroTuristaForm()
    return render(request, 'cuentas/registro.html', {'form': form})


# 2. Puente de redirección tras iniciar sesión (Nunca va a /admin)
@login_required
def redireccion_rol(request):
    rol = request.user.perfil.rol
    if rol == 'ADMIN':
        return redirect('panel_admin')
    elif rol == 'GUIA':
        return redirect('panel_guia')
    else:
        return redirect('panel_turista')


# 3. CRUD de Usuarios - Listar (Solo ADMIN)
@login_required
def lista_usuarios(request):
    if not es_admin(request.user):
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('redireccion_rol')

    # Mostramos todos los usuarios excepto los superusuarios/admins de consola
    usuarios = User.objects.filter(is_superuser=False).select_related('perfil')
    return render(request, 'cuentas/lista_usuarios.html', {'usuarios': usuarios})


# 4. CRUD de Usuarios - Crear Guía o Turista (Solo ADMIN)
@login_required
def crear_usuario(request):
    if not es_admin(request.user):
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('redireccion_rol')

    if request.method == 'POST':
        form = AdminCrearUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.perfil.rol = form.cleaned_data.get('rol')
            user.perfil.telefono = form.cleaned_data.get('telefono')
            user.perfil.save()
            messages.success(request, f"Usuario '{user.username}' creado con rol {user.perfil.get_rol_display()}.")
            return redirect('lista_usuarios')
    else:
        form = AdminCrearUsuarioForm()
    return render(request, 'cuentas/form_usuario.html', {'form': form, 'accion': 'Crear'})


# 5. CRUD de Usuarios - Editar (Solo ADMIN)
@login_required
def editar_usuario(request, user_id):
    if not es_admin(request.user):
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('redireccion_rol')

    usuario = get_object_or_404(User, id=user_id, is_superuser=False)

    if request.method == 'POST':
        form = AdminEditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save()
            user.perfil.rol = form.cleaned_data.get('rol')
            user.perfil.telefono = form.cleaned_data.get('telefono')
            user.perfil.save()
            messages.success(request, f"Datos de '{user.username}' actualizados correctamente.")
            return redirect('lista_usuarios')
    else:
        form = AdminEditarUsuarioForm(instance=usuario, initial={
            'rol': usuario.perfil.rol,
            'telefono': usuario.perfil.telefono
        })
    return render(request, 'cuentas/form_usuario.html', {'form': form, 'accion': 'Editar'})


# 6. CRUD de Usuarios - Eliminar (Solo ADMIN)
@login_required
def eliminar_usuario(request, user_id):
    if not es_admin(request.user):
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('redireccion_rol')

    usuario = get_object_or_404(User, id=user_id, is_superuser=False)
    nombre = usuario.username
    usuario.delete()
    messages.success(request, f"Usuario '{nombre}' eliminado del sistema.")
    return redirect('lista_usuarios')

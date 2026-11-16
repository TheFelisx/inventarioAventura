from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Perfil

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil y Rol'

    # Restringe las opciones para que desde aquí solo se asignen Guía o Turista
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "rol":
            kwargs['choices'] = [
                ('GUIA', 'Guía'),
                ('TURISTA', 'Turista'),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_rol', 'is_superuser')

    @admin.display(description='Rol')
    def get_rol(self, obj):
        return obj.perfil.get_rol_display() if hasattr(obj, 'perfil') else 'Sin perfil'

# Reemplazamos el UserAdmin por defecto para incluir el Perfil
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'telefono')
    list_filter = ('rol',)
    search_fields = ('usuario__username', 'usuario__email')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "rol":
            kwargs['choices'] = [
                ('GUIA', 'Guía'),
                ('TURISTA', 'Turista'),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

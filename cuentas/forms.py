from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Formulario público: cualquier visitante se registra solo (siempre nace como TURISTA)
class RegistroTuristaForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label="Nombre")
    last_name = forms.CharField(max_length=100, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# Formulario privado: el ADMIN crea Guías o Turistas desde su panel
class AdminCrearUsuarioForm(UserCreationForm):
    ROLES_PERMITIDOS = (
        ('GUIA', 'Guía'),
        ('TURISTA', 'Turista'),
    )
    first_name = forms.CharField(max_length=100, required=True, label="Nombre")
    last_name = forms.CharField(max_length=100, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    rol = forms.ChoiceField(choices=ROLES_PERMITIDOS, label="Rol asignado")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'rol']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# Formulario privado: el ADMIN edita los datos o cambia el rol de un usuario existente
class AdminEditarUsuarioForm(forms.ModelForm):
    ROLES_PERMITIDOS = (
        ('GUIA', 'Guía'),
        ('TURISTA', 'Turista'),
    )
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    rol = forms.ChoiceField(choices=ROLES_PERMITIDOS, label="Rol asignado")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

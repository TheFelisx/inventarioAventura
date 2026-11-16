from django import forms
from .models import Categoria, Experiencia

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'activo':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['titulo', 'descripcion', 'categoria', 'precio', 'cupo_maximo', 'fecha_hora', 'imagen_url', 'activo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'imagen_url': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com/foto.jpg'}),
        }
        labels = {'imagen_url': 'Imagen (link / URL)'}
        help_texts = {'imagen_url': 'Pega el enlace de una imagen. Si lo dejas vacío se muestra el ícono por defecto.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo permite elegir categorías que estén activas
        self.fields['categoria'].queryset = Categoria.objects.filter(activo=True)
        for name, field in self.fields.items():
            if name not in ['activo', 'fecha_hora']:
                field.widget.attrs['class'] = 'form-control'
            elif name == 'activo':
                field.widget.attrs['class'] = 'form-check-input'

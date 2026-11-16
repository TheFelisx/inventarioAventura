from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True) # True = Activo, False = Inactivo

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField()
    activo = models.BooleanField(default=True)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)  # link a la imagen (https://...)
    
    # Relaciones solicitadas
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='experiencias')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias_creadas')

    def __str__(self):
        return f"{self.titulo} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"


class Inscripcion(models.Model):
    ESTADOS_PAGO = (
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
    )

    turista = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=15, choices=ESTADOS_PAGO, default='PENDIENTE')

    class Meta:
        # Evita inscribirse dos veces en el mismo evento
        unique_together = ('turista', 'experiencia')

    def clean(self):
        # Evita que el turista reserve 2 eventos distintos el mismo día y a la misma hora
        if self.turista and self.experiencia:
            conflicto = Inscripcion.objects.filter(
                turista=self.turista,
                experiencia__fecha_hora=self.experiencia.fecha_hora
            ).exclude(pk=self.pk)

            if conflicto.exists():
                evento = conflicto.first().experiencia.titulo
                raise ValidationError(
                    f"Ya tienes una reserva programada para ese mismo día y hora: '{evento}'."
                )

    def save(self, *args, **kwargs):
        self.full_clean() # Ejecuta la validación antes de guardar en MySQL
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.turista.username} -> {self.experiencia.titulo} [{self.get_estado_pago_display()}]"


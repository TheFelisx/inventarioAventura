from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('GUIA', 'Guía'),
        ('TURISTA', 'Turista'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=15, choices=ROLES, default='TURISTA')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

# Crea automáticamente el Perfil como TURISTA al registrar un usuario nuevo (o ADMIN si es superuser)
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        rol_inicial = 'ADMIN' if instance.is_superuser else 'TURISTA'
        Perfil.objects.create(usuario=instance, rol=rol_inicial)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()

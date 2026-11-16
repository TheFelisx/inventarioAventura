from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiencias', '0002_experiencia_imagen'),
    ]

    operations = [
        # La imagen ahora se guarda como link (URL) en vez de subir un archivo
        migrations.RemoveField(
            model_name='experiencia',
            name='imagen',
        ),
        migrations.AddField(
            model_name='experiencia',
            name='imagen_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]

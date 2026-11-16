from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiencia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='experiencias/'),
        ),
    ]

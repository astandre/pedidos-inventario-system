# Generated by Django 2.1.7 on 2019-02-19 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidosHandler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='mesa',
            field=models.CharField(choices=[('AI', 'Afuera puerta izquierda'), ('AD', 'Afuera puerta derecha'), ('AT', 'Afuera televisor'), ('AM', 'Afuera meson'), ('AE', 'Afuera extra1'), ('B1', 'Adentro #1'), ('B2', 'Adentro #2'), ('B3', 'Adentro #3'), ('B4', 'Adentro #4'), ('B5', 'Adentro #5'), ('B6', 'Adentro #6'), ('B7', 'Adentro #7'), ('B8', 'Adentro #8'), ('B9', 'Adentro extra 1')], default='AI', max_length=2),
        ),
    ]

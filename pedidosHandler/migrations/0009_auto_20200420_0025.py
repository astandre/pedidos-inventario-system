# Generated by Django 3.0.5 on 2020-04-20 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidosHandler', '0008_auto_20200418_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.CharField(blank=True, default='CONSUMIDOR FINAL', max_length=100),
        ),
    ]

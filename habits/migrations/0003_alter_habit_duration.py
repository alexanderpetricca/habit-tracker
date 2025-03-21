# Generated by Django 5.1.6 on 2025-03-21 10:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_habit_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='duration',
            field=models.IntegerField(choices=[(7, '7'), (14, '14'), (30, '30'), (60, '60'), (120, '120'), (365, '365')], validators=[django.core.validators.MinValueValidator(7), django.core.validators.MaxValueValidator(365)]),
        ),
    ]

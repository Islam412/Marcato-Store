# Generated by Django 5.1.3 on 2025-01-20 19:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
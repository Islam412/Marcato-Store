# Generated by Django 4.2.19 on 2025-02-14 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0009_deliveryaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Primary', 'Primary'), ('Secondary', 'Secondary'), ('Third', 'Third')], max_length=20, verbose_name='Notes')),
                ('phone', models.CharField(max_length=30, verbose_name='Notes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_phone', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

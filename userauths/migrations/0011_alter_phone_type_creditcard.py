# Generated by Django 4.2.19 on 2025-02-14 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0010_alter_phone_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='type',
            field=models.CharField(choices=[('Primary', 'Primary'), ('Secondary', 'Secondary'), ('Third', 'Third')], max_length=20),
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=225)),
                ('country', models.CharField(max_length=225)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_credit_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

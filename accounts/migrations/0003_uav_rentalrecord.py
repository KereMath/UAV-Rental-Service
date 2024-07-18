# Generated by Django 5.0.7 on 2024-07-17 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UAV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('category', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RentalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('completed', 'Completed')], default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to=settings.AUTH_USER_MODEL)),
                ('uav', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='accounts.uav')),
            ],
        ),
    ]

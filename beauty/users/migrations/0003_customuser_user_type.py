# Generated by Django 5.1.7 on 2025-05-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('B', 'BARBER'), ('S', 'BARBERSHOP'), ('A', 'ADMIN'), ('U', 'COMMON_USER')], default='U', max_length=1, verbose_name='User Type'),
        ),
    ]

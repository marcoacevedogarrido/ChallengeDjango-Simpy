# Generated by Django 3.2.6 on 2021-08-10 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0004_alter_cashier_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='user',
        ),
    ]
# Generated by Django 3.2.6 on 2021-08-10 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0002_auto_20210809_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashier',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
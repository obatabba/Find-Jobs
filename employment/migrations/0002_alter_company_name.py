# Generated by Django 5.1.5 on 2025-01-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

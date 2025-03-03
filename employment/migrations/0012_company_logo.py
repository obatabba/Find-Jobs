# Generated by Django 5.1.6 on 2025-03-03 14:37

import employment.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0011_employee_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='companies/logo', validators=[employment.validators.validate_file_size]),
        ),
    ]

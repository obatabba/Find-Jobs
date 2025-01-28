# Generated by Django 5.1.5 on 2025-01-28 14:21

import employment.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0007_application_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.FileField(upload_to='employment/resumes', validators=[employment.validators.validate_file_size, employment.validators.validate_file_content]),
        ),
    ]

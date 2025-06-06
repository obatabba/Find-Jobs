# Generated by Django 5.1.6 on 2025-03-05 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0012_company_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='tags',
            field=models.ManyToManyField(related_name='+', to='employment.tag'),
        ),
    ]

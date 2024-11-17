# Generated by Django 5.1.3 on 2024-11-17 01:31

import django_jsonform.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directoryName', models.CharField(max_length=200, verbose_name='Название справочника')),
                ('directoryItems', django_jsonform.models.fields.JSONField(verbose_name='Элементы справочника')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
    ]

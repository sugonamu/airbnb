# Generated by Django 5.1.1 on 2024-09-30 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_property_property_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='property_type',
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-16 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('join_api', '0020_contact_color_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='color_name',
        ),
    ]

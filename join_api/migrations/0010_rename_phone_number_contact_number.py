# Generated by Django 5.1.4 on 2025-01-07 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('join_api', '0009_rename_number_contact_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='phone_number',
            new_name='number',
        ),
    ]

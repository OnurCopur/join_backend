# Generated by Django 5.1.4 on 2025-01-09 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join_api', '0016_alter_task_category_alter_task_contacts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.TextField(blank=True, default='[]'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-09 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join_api', '0011_remove_task_prioicon_alter_task_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]

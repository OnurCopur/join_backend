# Generated by Django 5.1.4 on 2025-01-01 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join_api', '0003_alter_task_prio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='color',
        ),
        migrations.AlterField(
            model_name='task',
            name='contacts',
            field=models.ManyToManyField(blank=True, to='join_api.contact'),
        ),
    ]

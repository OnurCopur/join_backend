# Generated by Django 5.1.4 on 2025-01-09 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join_api', '0010_rename_phone_number_contact_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='prioIcon',
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('Technical Task', 'Technical Task'), ('User Story', 'User Story')], max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='contacts',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='join_api.contact'),
        ),
        migrations.AlterField(
            model_name='task',
            name='phases',
            field=models.CharField(default='To Do', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]

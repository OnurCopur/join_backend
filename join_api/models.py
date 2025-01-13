from django.db import models


# Modell für Kontakte
class Contact(models.Model):
    color = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[('Technical Task', 'Technical Task'), ('User Story', 'User Story')])
    contacts = models.ManyToManyField('Contact', related_name='tasks', blank=True)
    date = models.DateField()
    prio = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('Urgent', 'Urgent')])
    phases = models.CharField(max_length=50, default='To Do')
    subtasks = models.TextField(blank=True, default="[]") 
    prioIcon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

# Modell für Benutzer
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)  # Speichern des Passworts (sicher verschlüsseln!)

    def __str__(self):
        return self.name

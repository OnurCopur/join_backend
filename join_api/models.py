from django.db import models

# Create your models here.

class Contact(models.Model):
    color = models.CharField(max_length=20)  # Hex oder Name des Farbcodes
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nummer = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', 'Urgent'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    contacts = models.ManyToManyField(Contact, related_name='tasks')  # Many-to-Many-Beziehung
    date = models.DateField()  # Erstellungs- oder Fälligkeitsdatum
    phases = models.CharField(max_length=100)  # Evtl. für Phasen wie "To Do", "In Progress"
    prio = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    prioIcon = models.CharField(max_length=100)  # Für den Icon-Pfad oder Symbolnamen
    subtasks = models.JSONField(blank=True, default=list)  # Liste von Unteraufgaben

    def __str__(self):
        return self.title
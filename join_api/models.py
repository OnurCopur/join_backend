from django.db import models


# Modell für Kontakte
class Contact(models.Model):
    color = models.CharField(max_length=20, null=True, choices=[
        ("#3380FF", "#3380FF"),
        ("#1d6331", "#1d6331"),
        ("#FFEA33", "#FFEA33"),
        ("#FF5733", "#FF5733"),
        ("#7A33FF", "#7A33FF"),
        ("#FF33C1", "#FF33C1"),
        ("#33E6FF", "#33E6FF"),
        ("#FF33A2", "#FF33A2"),
        ("#33FFF1", "#33FFF1"),
    ])
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
    prioIcon = models.CharField(max_length=255, blank=True, null=True)
    category_color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

    

# Modell für Subtask
class Subtask(models.Model):
    task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
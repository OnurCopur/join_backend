from rest_framework import serializers
from .models import Task, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)  # Nested Serializer für die Kontakte

    class Meta:
        model = Task
        fields = '__all__'

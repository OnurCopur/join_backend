from rest_framework import serializers
from .models import Task, Contact, User
import json


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'number', 'color']
        

class TaskSerializer(serializers.ModelSerializer):
    contacts = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, required=False)  # Kontakte als IDs
    subtasks = serializers.JSONField(default=list, required=False)  # Standardwert für Subtasks ist ein leeres Array
    prioIcon = serializers.CharField(required=False, read_only=True)  # prioIcon als readonly
    category_color = serializers.SerializerMethodField()  # Neu: Farbe basierend auf der Kategorie

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'contacts', 'date', 'phases', 'prio', 'subtasks', 'prioIcon', 'category_color']  # Neu: category_color hinzufügen

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Subtasks von JSON-String in ein Array umwandeln
        representation['subtasks'] = json.loads(instance.subtasks or '[]')
        return representation

    def validate_subtasks(self, value):
        # Sicherstellen, dass die Subtasks als JSON-Array vorliegen
        if not isinstance(value, list):
            raise serializers.ValidationError("Subtasks müssen ein Array sein.")
        return json.dumps(value)  # Speichern als JSON-String

    def create(self, validated_data):
        # Kontakte und Subtasks aus den validierten Daten extrahieren
        contacts_data = validated_data.pop('contacts', [])
        subtasks_data = validated_data.pop('subtasks', [])

        # Priorität extrahieren und Standardwert setzen
        prio = validated_data.get('prio', None)

        # prioIcon basierend auf der Priorität setzen
        if prio == 'Low':
            validated_data['prioIcon'] = '/img/PrioBajaGreen.svg'
        elif prio == 'Medium':
            validated_data['prioIcon'] = '/img/PrioMediaOrange.svg'
        elif prio == 'Urgent':
            validated_data['prioIcon'] = '/img/PrioAltaRed.svg'
        else:
            validated_data['prioIcon'] = ''  # Standardwert, falls keine Priorität gesetzt wurde

        # Task erstellen
        task = Task.objects.create(**validated_data)

        # Kontakte korrekt zuweisen
        task.contacts.set(contacts_data)

        # Subtasks speichern (als JSON-Array)
        task.subtasks = subtasks_data if subtasks_data is not None else []
        task.save()

        return task


    def get_category_color(self, obj):
        # Gebe die Farbe basierend auf der Kategorie zurück
        if "User Story" in obj.category:
            return "blue"
        elif "Technical Task" in obj.category:
            return "green"
        return "default"  # Fallback für alle anderen Kategorien





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

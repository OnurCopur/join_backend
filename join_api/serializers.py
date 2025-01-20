from rest_framework import serializers
from .models import Task, Contact
import json


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'number', 'color']

    def to_representation(self, instance):
        """
        Überschreiben der `to_representation`-Methode, um den Farbcode zusammen mit dem Farbname als Hinweis zu formatieren.
        """
        representation = super().to_representation(instance)
        # Mapping für den Farbcode zu Namen
        color_map = {
            "#3380FF": "Blue",
            "#1d6331": "Green",
            "#FFEA33": "Yellow",
            "#FF5733": "Red",
            "#7A33FF": "Purple",
            "#FF33C1": "Pink",
            "#33E6FF": "Cyan",
            "#FF33A2": "Magenta",
            "#33FFF1": "Turquoise"
        }
        
        # Farbcode als Hinweis
        color_code = representation['color']
        color_name = color_map.get(color_code, "Unknown")
        
        # Zum Beispiel: Code + Name als Hinweis zurückgeben (optional für Anzeige)
        representation['color_info'] = f"{color_name} ({color_code})"
        
        return representation


        

class TaskSerializer(serializers.ModelSerializer):
    contacts = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, required=False)
    subtasks = serializers.JSONField(default=list, required=False)
    prioIcon = serializers.CharField(required=False, read_only=True)
    category_color = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'contacts', 'date', 'phases', 'prio', 'subtasks', 'prioIcon', 'category_color']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subtasks'] = json.loads(instance.subtasks or '[]')
        return representation

    def validate_subtasks(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Subtasks müssen ein Array sein.")
        return json.dumps(value)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', [])
        subtasks_data = validated_data.pop('subtasks', [])
        prio = validated_data.get('prio', None)

        if prio == 'Low':
            validated_data['prioIcon'] = '/img/PrioBajaGreen.svg'
        elif prio == 'Medium':
            validated_data['prioIcon'] = '/img/PrioMediaOrange.svg'
        elif prio == 'Urgent':
            validated_data['prioIcon'] = '/img/PrioAltaRed.svg'
        else:
            validated_data['prioIcon'] = ''

        task = Task.objects.create(**validated_data)
        task.contacts.set(contacts_data)
        task.subtasks = subtasks_data if subtasks_data is not None else []
        task.save()
        return task

    def update(self, instance, validated_data):
        # Update der vorhandenen Felder
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.contacts.set(validated_data.get('contacts', instance.contacts.all()))  # Kontakte aktualisieren
        instance.subtasks = validated_data.get('subtasks', instance.subtasks)
        instance.phases = validated_data.get('phases', instance.phases)  # Phase aktualisieren
        instance.save()
        return instance

    
    def get_category_color(self, obj):
        # Gebe die Farbe basierend auf der Kategorie zurück
        if "User Story" in obj.category:
            return "blue"
        elif "Technical Task" in obj.category:
            return "green"
        return "default"  # Fallback für alle anderen Kategorien

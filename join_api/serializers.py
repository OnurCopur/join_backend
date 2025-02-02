from rest_framework import serializers
from .models import Task, Contact, Subtask
import json


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'number', 'color']

    def to_representation(self, instance):
        """
        Überschreiben der to_representation-Methode, um den Farbcode zusammen mit dem Farbname als Hinweis zu formatieren.
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
    

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'completed']


        

class TaskSerializer(serializers.ModelSerializer):
    contacts = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, required=False)
    subtasks = SubtaskSerializer(many=True, required=False) 
    prioIcon = serializers.CharField(required=False, read_only=True)
    category_color = serializers.SerializerMethodField()

    date = serializers.DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'], format='%Y-%m-%d')


    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'contacts', 'date', 'phases', 'prio', 'subtasks', 'prioIcon', 'category_color']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subtasks'] = SubtaskSerializer(instance.subtasks.all(), many=True).data
        return representation

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        contacts_data = validated_data.pop('contacts', [])
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

        # Subtasks erstellen und sicherstellen, dass IDs erhalten bleiben
        for subtask_data in subtasks_data:
            # Überprüfe, ob eine ID vorhanden ist, um den Subtask zu aktualisieren oder zu erstellen
            if 'id' in subtask_data:
                subtask = Subtask.objects.get(id=subtask_data['id'])
                subtask.title = subtask_data.get('title', subtask.title)
                subtask.completed = subtask_data.get('completed', subtask.completed)
                subtask.save()
            else:
                # Wenn keine ID vorhanden ist, erstelle einen neuen Subtask
                Subtask.objects.create(task=task, **subtask_data)

        return task


    def update(self, instance, validated_data):
        # Update der vorhandenen Felder
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.contacts.set(validated_data.get('contacts', instance.contacts.all()))  # Kontakte aktualisieren
        instance.phases = validated_data.get('phases', instance.phases)  # Phase aktualisieren
        instance.date = validated_data.get('date', instance.date)

                # Prioritäts-Icon aktualisieren
        prio = validated_data.get('prio', instance.prio)
        instance.prio = prio
        if prio == 'Low':
            instance.prioIcon = '/img/PrioBajaGreen.svg'
        elif prio == 'Medium':
            instance.prioIcon = '/img/PrioMediaOrange.svg'
        elif prio == 'Urgent':
            instance.prioIcon = '/img/PrioAltaRed.svg'
        else:
            instance.prioIcon = ''  # Fallback für unklare Priorität

        # Bestehende Subtasks aktualisieren oder neu erstellen
        subtasks_data = validated_data.get('subtasks', [])
        existing_subtasks = {subtask.id: subtask for subtask in instance.subtasks.all()}

        # Überprüfe jede übergebene Subtask-Daten
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id', None)

            if subtask_id and subtask_id in existing_subtasks:
                # Subtask existiert bereits, also aktualisiere sie
                subtask = existing_subtasks[subtask_id]
                subtask.title = subtask_data.get('title', subtask.title)
                subtask.completed = subtask_data.get('completed', subtask.completed)
                subtask.save()
                del existing_subtasks[subtask_id]  # Entferne diese Subtask aus der Liste der existierenden Subtasks
            else:
                # Wenn die Subtask nicht existiert, erstelle sie
                Subtask.objects.create(task=instance, **subtask_data)

        # Alle verbleibenden Subtasks (die nicht mehr im Request sind) löschen
        for remaining_subtask in existing_subtasks.values():
            remaining_subtask.delete()

        instance.save()
        return instance


    
    def get_category_color(self, obj):
        # Gebe die Farbe basierend auf der Kategorie zurück
        if "User Story" in obj.category:
            return "blue"
        elif "Technical Task" in obj.category:
            return "green"
        return "default"  # Fallback für alle anderen Kategorien
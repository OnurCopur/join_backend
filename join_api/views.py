from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Contact
from .serializers import TaskSerializer, ContactSerializer
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdmin, IsAuthenticated, IsStaffOrReadOnly


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Überschreibt die create-Methode, um benutzerdefinierte Fehlerbehandlung hinzuzufügen.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Überschreibt die update-Methode, um benutzerdefinierte Fehlerbehandlung hinzuzufügen.
        """
        partial = kwargs.pop('partial', False)  # Für teilweise Updates
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request):
        """
        Löscht alle Aufgaben.
        """
        Task.objects.all().delete()
        return Response({'message': 'All tasks have been deleted.'}, status=status.HTTP_204_NO_CONTENT)


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Überschreibt die create-Methode, um benutzerdefinierte Fehlerbehandlung hinzuzufügen.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request):
        """
        Löscht alle Kontakte.
        """
        Contact.objects.all().delete()
        return Response({'message': 'All contacts have been deleted.'}, status=status.HTTP_204_NO_CONTENT)
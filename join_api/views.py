from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Contact, User
from .serializers import TaskSerializer, ContactSerializer, UserSerializer
from rest_framework.decorators import action


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        """
        Überschreibt die `create`-Methode, um benutzerdefinierte Fehlerbehandlung hinzuzufügen.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    def create(self, request, *args, **kwargs):
        """
        Überschreibt die `create`-Methode, um benutzerdefinierte Fehlerbehandlung hinzuzufügen.
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

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Überschreibt die `create`-Methode, um benutzerdefinierte Fehlerbehandlung hinzuzufügen.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

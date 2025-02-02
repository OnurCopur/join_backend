from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, GuestLoginSerializer
from rest_framework.permissions import AllowAny


class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Benutzer erstellen
            token, created = Token.objects.get_or_create(user=user)  # Token generieren
            # Rückgabe von Benutzerdaten und Token
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "token": token.key
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Benutzerdefinierte Authentifizierungsmethode
def authenticate_by_email(email, password):
    try:
        # Suche nach dem Benutzer mit der E-Mail
        user = User.objects.get(email=email)
        # Überprüfe das Passwort des Benutzers
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
    return None

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate_by_email(email=email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({
                    'token': token.key,
                    'username': user.username,
                    'email': user.email  # Benutzername hier hinzufügen
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GuestLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=200)
        return Response(serializer.errors, status=400)
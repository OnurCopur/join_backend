from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ContactViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

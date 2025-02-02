from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]

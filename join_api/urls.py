from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, TaskListView


router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = router.urls

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
]

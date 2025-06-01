from django.urls import path
from .api_views import ProjectListCreateAPIView

urlpatterns = [
    path('project/', ProjectListCreateAPIView.as_view(), name='project-api'),
]

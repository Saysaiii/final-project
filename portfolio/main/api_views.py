from rest_framework.generics import ListCreateAPIView
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
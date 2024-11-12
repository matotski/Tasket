from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Project, Task
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer


# def index(request):
#     context = {
#         "users": User.objects.all(),
#         "projects": Project.objects.all(),
#         "tasks": Task.objects.all()
#     }
#     return render(request, 'index.html', context=context)

class UserApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get(self, request):
        u = User.objects.all()
        return Response({"posts" : UserSerializer(u, many=True).data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error" : "Object does not exists"})

        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

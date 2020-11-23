from django.http import Http404
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TaskSerializer, UserLoginSerializer, UserRegisterSerializer
from .models import Task, User


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(id=self.kwargs['pk'], user=user)


class LoginView(ObtainAuthToken):
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })


class RegisterView(APIView):
    permission_classes = ()
    serializer_class = UserRegisterSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        }, status=201)


"""Вместо добавления разных эндпоинтов для добавления записи 
и получения списка записей предпочитаю обьединять в 1 принимающий как get так и post запросы"""
class TaskListView2(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

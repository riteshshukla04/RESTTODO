from re import search
from rest_framework import serializers
from rest_framework.utils import serializer_helpers
from accounts.serializers import UserSearlizers,LoginSerializer
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from django.contrib import auth
from django.conf import settings
import jwt

class Registerview(GenericAPIView):
    serializer_class=UserSearlizers
    def post(self,request):
        serializers=UserSearlizers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            

            serializer = UserSearlizers(user)

            data = {'user': serializer.data}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Task

from .serializers import TaskSerializer
from rest_framework import permissions


class ContactList(ListCreateAPIView):

    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class ContactDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
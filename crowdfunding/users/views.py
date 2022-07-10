# from django.shortcuts import render
from functools import partial
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
# Added 4Jul2022; doesnt work
# from .permissions import IsOwnerOrReadOnly

# Create your views here.

class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors)

class CustomUserDetail(APIView):

    # Added 4Jul2022; Copied from project; Doesnt work!
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly
    # ]
        
    # def get_object(self, pk):
    #     try:
    #         user = CustomUser.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, user)
    #         return user
    #     except CustomUser.DoesNotExist:
    #         raise Http404

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

     # Added 4Jul2022
    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True           
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )




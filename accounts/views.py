from django.contrib.auth import login
#from django.http import HttpResponse, HttpResponseRedirect
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import (LoginSerializer, PasswordChangeSerializers,
                          RegisterSerializer, UserSerializer)


class UserListAPI(generics.ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
 

class UserDetailAPI(generics.RetrieveAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class LoginAPI(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class PasswordChangeAPI(generics.UpdateAPIView):
    
    serializer_class = PasswordChangeSerializers
    permission_classes = (IsAuthenticated, )
    
    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #delete users all tokens so that user will be logged out all sessions after password change
        AuthToken.objects.filter(user=user).delete()

        return Response(#status=status.HTTP_200_OK,  
                        {"token": AuthToken.objects.create(user)[1]
                        })


from rest_framework import generics
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
 
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

  def post(self, request, *args, **kwargs):

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    token = AuthToken.objects.create(user)[1]
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })


class RegisterAPI(generics.GenericAPIView):

  serializer_class = RegisterSerializer
  queryset = UserProfile.objects.all()

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })

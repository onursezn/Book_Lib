from datetime import timedelta

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.views import \
    get_password_reset_token_expiry_time
#from django.http import HttpResponse, HttpResponseRedirect
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .permissions import IsOwnProfileOrReadOnly
from .serializers import (CustomTokenSerializer, LoginSerializer,
                          PasswordChangeSerializers, RegisterSerializer,
                          UserDetailsSerializer, UserSerializer)


class UserListAPI(generics.ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class UserDetailAPI(generics.RetrieveUpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnProfileOrReadOnly,)
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailsSerializer
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
        "token": AuthToken.objects.create(user)[1]}, 
        status=status.HTTP_200_OK)


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
        }, status=status.HTTP_201_CREATED)


class PasswordChangeAPI(generics.UpdateAPIView):
    
    serializer_class = PasswordChangeSerializers
    permission_classes = (IsAuthenticated, )
    
    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #delete users all tokens so that user will be logged out all sessions after password change
        AuthToken.objects.filter(user=user).delete()

        return Response({"token": AuthToken.objects.create(user)[1] }, 
                        status=status.HTTP_200_OK)


class CustomPasswordResetView:

    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "http://127.0.0.1:8000/accounts/password-reset/{}".format(reset_password_token.key),
            'site_name': 'http://127.0.0.1:8000/',
            'site_domain': ''
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for bookapp", #.format(site_full_name),
            # message:
            email_plaintext_message,
            # from:
            "noreply@bookapp.com",#.format(site_url),
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()


class CustomPasswordTokenVerificationView(APIView):
    """
      An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
      reset.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomTokenSerializer
    #permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'invalid'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        # check if user has password to change
        if not reset_password_token.user.has_usable_password():
            return Response({'status': 'irrelevant'})

        return Response({'status': 'OK'})

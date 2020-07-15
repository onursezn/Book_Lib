from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'username', 'email',)


class UserDetailsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'username', 'email',)
        read_only_fields = ('email', 'username')


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True) #style = {'input_type':'password'})

    class Meta:
      model = UserProfile
      fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')
      extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
      password = self.validated_data['password']
      confirm_password = self.validated_data['confirm_password']
      if password == confirm_password:
        user = UserProfile.objects.create_users(email = validated_data['email'], 
                                              username = validated_data['username'],  
                                              password = password,
                                              first_name = validated_data['first_name'],
                                              last_name = validated_data['last_name'])
        return user

      raise serializers.ValidationError("Passwords must match")
      

class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
      user = authenticate(**data)
      if user and user.is_active:
        return user
      raise serializers.ValidationError("Incorrect Credentials")
  

class PasswordChangeSerializers(serializers.Serializer):

    old_password = serializers.CharField(max_length=128, write_only=True, required=True)#style = {'input_type':'password'})
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)#style = {'input_type':'password'})
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)#style = {'input_type':'password'})

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Your old password is incorrect. Please try again.')
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords mismatch. Please try again")
        validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


#token serializer for email password reset endpoint
class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
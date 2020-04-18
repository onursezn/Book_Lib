from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth import authenticate

 
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'username', 'email',)


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'username', 'email',)
        read_only_fields = ('email', )


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.SerializerMethodField()
    user = UserDetailsSerializer()

    def get_token(self, obj):
      return obj["token"][1]


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True) #style = {'input_type':'password'})

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
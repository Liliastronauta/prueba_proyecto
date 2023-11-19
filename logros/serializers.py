from rest_framework import serializers
from logros.models import User
from logros.models import Achievements
from rest_framework import viewsets, serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'user_name', 'birth_date', 'email', 'password'] 

    def validate(self, attrs):
    
        email = attrs.get('email', '')
        user_name=attrs.get('user_name', '')

        if not user_name.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs
    
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



"""class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= '__all__' """


class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'    








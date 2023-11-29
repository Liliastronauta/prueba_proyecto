from rest_framework import serializers
from logros.models import User
from logros.models import Achievements, Profile
from rest_framework import viewsets, serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from drf_extra_fields.fields import Base64ImageField
from datetime import datetime
from dateutil.relativedelta import relativedelta

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'user_name', 'birth_date', 'email', 'password'] 
    
    def validate_birth_date(self, birth_date):
        age=relativedelta(datetime.now(), birth_date).years

        if age < 18:
            raise serializers.ValidationError('Must be at least 18 years old to register.')
        else:
            return birth_date

    def validate(self, attrs):
    
        email = attrs.get('email', '')
        user_name=attrs.get('user_name', '')

        if not user_name.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs
    
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'    

class AchievementImageSerializer(serializers.ModelSerializer):
    image=Base64ImageField(required=False)
    class Meta:
        model= Achievements
        fields= '__all__' 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= '__all__' 

class ProfileImageSerializer(serializers.ModelSerializer):
    profile_picture=Base64ImageField(required=False)
    class Meta:
        model= Profile
        fields= '__all__' 








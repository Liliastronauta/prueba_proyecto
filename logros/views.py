from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from rest_framework import status, generics, viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from logros.models import User, Achievements
from logros.serializers import  AchievementsSerializer, RegisterSerializer
import random
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from logros.utils import Util
from django.urls import reverse
import jwt
from django.conf import settings

# Create your views here.


#Registro de Usuario
class RegisterView(generics.GenericAPIView):

    serializer_class= RegisterSerializer

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data= serializer.data
        user=User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token

        current_site= get_current_site(request).domain
        relativeLink=reverse('email-verify')

        absurl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body='Welcome to AhsokaVoice '+user.user_name+' Please use the link below to verify your email\n'+ absurl
        data={'email_body':email_body,'to_email':user.email, 'email_subject':'Verify your email'}

        Util.send_email(data)


        return Response(user_data, status=status.HTTP_201_CREATED )
    
class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token, settings.SECRET_KEY)
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':' Successfully activated'}, status=status.HTTP_200_OK )
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':' Activation Expired'}, status=status.HTTP_400_BAD_REQUEST )
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':' Invalid Token '}, status=status.HTTP_400_BAD_REQUEST )


"""class RetriveUsers(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        users_list = Users.objects.all()
        serializer = UsersSerializer(users_list, many=True)
        return Response(serializer.data)"""


class RetriveAchievements(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        achievements_list = Achievements.objects.all()
        serializer = AchievementsSerializer(achievements_list, many=True)
        return Response(serializer.data)
    
    # Eliminar logro
    def delete(self, request, achievement_id):
        achievement_obj = get_object_or_404(Achievements, pk=achievement_id)
        achievement_obj.status = False
        achievement_obj.save()
        return Response({'message':'Eliminado'}, status=status.HTTP_204_NO_CONTENT)


"""class CreateUser(APIView): #Funcionando
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Creado'}, status=status.HTTP_201_CREATED)"""

class CreateAchieve(APIView): #Funcionando
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = AchievementsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'Creado'} , status=status.HTTP_201_CREATED)


# Logro: lista.feed Mostrar un logro aleatorio
class RetriveRandom(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        achievements_list = Achievements.objects.all()

        if achievements_list.exists():      
            max_id = achievements_list.aggregate(max_id=Max("id"))['max_id']
            pk = random.randint(1, max_id+1)
            random_achievement = Achievements.objects.get(pk=pk)
            serializer = AchievementsSerializer(random_achievement)
            return Response(serializer.data)
        else:
            return Response({'message':'No achievements available'}, status=status.HTTP_404_NOT_FOUND)

#Funcionalidad lista.all
class ListAchievementsView(APIView):
    permission_classes=(AllowAny,)

    def get(self, request):
        achievements_list = Achievements.objects.all()
        serializer= AchievementsSerializer(achievements_list, many=True)
        return Response(serializer.data)

#Editar logro
class EditAchievement(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, achievement_id):
        achievement_obj = get_object_or_404(Achievements, pk=achievement_id)
        serializer = AchievementsSerializer(achievement_obj)
        return Response(serializer.data)

    def put(self, request, achievement_id):
        achievement_obj = get_object_or_404(Achievements, pk=achievement_id)
        serializer = AchievementsSerializer (instance=achievement_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#Imagen
def achievementsimage(request, achievementsimage_id):
    achievementsimage= Achievements.objects.get(pk=achievementsimage_id)
    if achievementsimage is not None:
        return render(request, 'achievementsimage/achievementsimage.html', {'achievementsimage':achievementsimage})
    else:
        raise Http404('logro does not exist')
    






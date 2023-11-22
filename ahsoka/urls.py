"""
URL configuration for ahsoka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from logros.views import RetriveAchievements , CreateAchieve, RetriveRandom, ListAchievementsView, EditAchievement, AchievementImageJson, ProfileImageJson, CreatePerfil, EditProfile
from logros import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('achievements/', RetriveAchievements.as_view()), #Logros
    path('achievements/create', CreateAchieve.as_view()),  #Craer Logro
    path('achievements/random', RetriveRandom.as_view()),  #Listar logros random
    path('achievements/list/', ListAchievementsView.as_view()), #Listar todos los logros
    path('achievements/edit/<int:achievement_id>/', EditAchievement.as_view()), #Editar Logros

    path('auth/', include('logros.urls')), #Registro
    path('image_achievements/', AchievementImageJson.as_view()), #Imagen de logros
    path('profile/create/', CreatePerfil.as_view()), #Crear perfil
    #path('profile/edit/', EditProfile.as_view()), #Editar perfil
    path('image_profile/', ProfileImageJson.as_view()) #Imagen del perfil 
    
   ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


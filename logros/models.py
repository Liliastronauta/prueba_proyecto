from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _




# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, first_name, last_name, user_name, birth_date, email, password=None):
        """
        Create and save a user with the given email and password.
        """
        if not first_name:
            raise ValueError(_("The first name must be set"))
        if not last_name:
            raise ValueError(_("The last name must be set"))
        if not user_name:
            raise ValueError(_("The username must be set"))
        if not birth_date:
            raise ValueError(_("The birthday date must be set"))
        if not email:
            raise ValueError(_("The email must be set"))
        
        email = self.normalize_email(email)
        user = self.model( first_name=first_name, last_name=last_name, user_name=user_name, birth_date=birth_date ,email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.save()
        return user
        

    def create_superuser(self, first_name , last_name, user_name, birth_date, email, password=None):
        """
        Create and save a SuperUser with the given email and password.
        
        """
        if not password:
            raise ValueError(_("The password must be set"))
        user= self.create_user(first_name, last_name, user_name, birth_date ,email, password)
        user.is_superuser=True
        user.is_staff = True
        user.save()
        return user

    

class User(AbstractBaseUser, PermissionsMixin ):
    first_name= models.CharField(max_length=50, verbose_name="nombre", null=True)
    last_name= models.CharField(max_length=50, verbose_name="apellido", null=True)
    user_name=models.CharField(max_length=200, verbose_name="usuario", unique=True, db_index=True)
    birth_date= models.DateField(verbose_name="fecha de nacimiento", null=True)
    email= models.EmailField(max_length=200, verbose_name="email", unique=True)
    password=models.CharField(max_length=200, verbose_name="password")

    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['first_name', 'last_name', 'user_name', 'birth_date', 'password']
    objects=UserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        return ''


    class Meta:
        db_table= 'User'        



class Achievements(models.Model):
    achievement= models.CharField(max_length=300, verbose_name="logro")
    date=models.DateField(verbose_name="fecha")
    idarea= models.IntegerField(default=0, verbose_name="id area")
    description= models.CharField(max_length=500, verbose_name="descripcion")
    image= models.ImageField(upload_to='logros/files/image_achievement' ,null=True, blank=True, verbose_name='imagen')
    iduser= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id user')


    class Meta:
        db_table='Achievements'


class Profile(models.Model):
    profile_picture=models.ImageField(verbose_name="imagen perfil")
    bio=models.CharField(max_length=300, verbose_name="biografia")  
    iduser= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id user')  

    class Meta:
        db_table="Profile"  

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,username,poste,password = None):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Users should have a username')
        if not poste:
            raise ValueError('Users should have a poste')

        user = self.model(
            email =self.normalize_email(email),
            username = username,
            poste = poste
            )

        user.set_password(password)
        user.save(using = self._db)
        return user
 
    def create_superuser(self,email,username,poste,password = None):
        print('*****   creating the supter user   ******')
        user = self.create_user(
            email =self.normalize_email(email),
            username = username,
            poste = poste,
            password = password
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="Email Address",max_length=60,unique=True)
    date_joined = models.DateTimeField(verbose_name="Date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login",auto_now=True)    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    societe = models.IntegerField(default=0)
    poste = models.CharField(max_length=15)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username','poste']

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
    
    def has_perm(self,perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True


class Societe(models.Model):
    nom = models.CharField(max_length=60)
    localisation = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    date_creation = models.DateField()

    def __str__(self):
        return self.nom


class Agent(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=60)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    statut = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

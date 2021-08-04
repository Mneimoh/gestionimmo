# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# class UserManager(BaseUserManager):
#     def create_user(self,email,username,password = None):
#         if not email:
#             raise ValueError('Email is required')
#         if not username:
#             raise ValueError('Users should have a username')
#         user = self.model(
#             email =self.normalize_email(email),
#             username = username,
#             )

#         user.set_password(password)
#         user.save(using = self._db)
#         return user
 
#     def create_superuser(self,email,username,password):
#         print('*****   creating the supter user   ******')
#         user = self.create_user(
#             email =self.normalize_email(email),
#             username = username,
#             password = password
#         )

#         user.is_superuser = True
#         user.is_admin = True
#         user.is_staff = True
#         user.save(using = self._db)
#         return user


# class User(AbstractBaseUser):
#     username            = models.CharField(max_length=255)
#     email               = models.EmailField(verbose_name="Email Address",max_length=60,unique=True)
#     date_joined         = models.DateTimeField(verbose_name="Date joined",auto_now_add=True)
#     last_login          = models.DateTimeField(verbose_name="Last login",auto_now=True)    
#     is_admin            = models.BooleanField(default=False)
#     is_active           = models.BooleanField(default=True)
#     is_staff            = models.BooleanField(default=True)
#     is_superuser        = models.BooleanField(default=False)
#     societe             = models.IntegerField(default=0)
#     # poste               = models.CharField(max_length=15)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username

#     def has_perm(self,perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self,app_label):
#         return True

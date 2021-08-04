from django.db import models

# Create your models here.

# class Societe(models.Model):
#     nom = models.CharField(max_length=60)
#     localisation = models.CharField(max_length=200)
#     active = models.BooleanField(default=False)
#     date_creation = models.DateField()

#     def __str__(self):
#         return self.nom


# class Agent(models.Model):
#     societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
#     login = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     email = models.EmailField(max_length=60)
#     nom = models.CharField(max_length=30)
#     prenom = models.CharField(max_length=30)
#     statut = models.CharField(max_length=20)
#     active = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.nom







# class Societe(models.Model):
#     nom             = models.CharField(max_length=60)
#     localisation    = models.CharField(max_length=200)
#     active          = models.BooleanField(default=False)
#     date_creation   = models.DateTimeField(verbose_name="Date joined",auto_now_add=True)

#     def __str__(self):
#         return self.nom


# class Agent(models.Model):
#     societe         = models.ForeignKey(Societe, on_delete=models.CASCADE)
#     poste           = models.CharField(max_length=15)
#     login           = models.CharField(max_length=20)
#     password        = models.CharField(max_length=20)
#     email           = models.EmailField(max_length=60)
#     nom             = models.CharField(max_length=30)
#     prenom          = models.CharField(max_length=30)
#     statut          = models.CharField(max_length=20)
#     active          = models.BooleanField(default=False)
#     created_at      = models.DateTimeField(auto_now_add=True)
#     updated_at      = models.DateTimeField(auto_now=True)
    



#     def __str__(self):
#         return self.nom


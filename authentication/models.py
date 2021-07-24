from django.db import models

# Create your models here.
class User(models.Model):
    societe = models.IntegerField(default=0)
    login = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=60)
    poste = models.CharField(max_length=15)
    active = models.BooleanField(default=False)
    date_creation = models.DateField()

    def __str__(self):
        return self.login
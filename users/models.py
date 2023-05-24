from django.db import models
from django.contrib.auth.models import AbstractUser

class Transactions(models.Model):
    sender = models.CharField(verbose_name="Remetente", max_length=100)
    amount = models.FloatField(verbose_name="Valor")

class CustomUser(AbstractUser):
    wallet = models.FloatField(verbose_name="Carteira")
    transactions = models.ManyToManyField(Transactions)

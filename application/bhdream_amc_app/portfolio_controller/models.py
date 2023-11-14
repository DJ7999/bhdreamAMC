
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User

class Equity(models.Model):
    symbol = models.CharField(max_length=20, unique=True, blank=False)
    title=models.CharField(max_length=100,unique=True, blank=False)

class Investment(models.Model):
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    shares = models.PositiveIntegerField(null=False, blank=False)
    investment_date = models.DateField()
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)             
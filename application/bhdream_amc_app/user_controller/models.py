from django.db import models
from django.core.exceptions import ValidationError
from rest_framework import serializers

# UserProfile Model
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username

# Investment Model
class EquitySymbol(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol

class Investment(models.Model):
    ASSET_TYPE_CHOICES = [
        ('FD', 'Fixed Deposit'),
        ('Equity', 'Equity Investment'),
    ]

    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)                                            #c
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES)                                       #c
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)                    #fd
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)                    #equity
    shares = models.PositiveIntegerField(null=True, blank=True)                                                     #equity
    investment_date = models.DateField()                                                                            #c
    maturity_date = models.DateField(null=True, blank=True)                                                         #fd
    equity_symbol = models.ForeignKey(EquitySymbol, on_delete=models.SET_NULL, null=True, blank=True)               #equity

    def __str__(self):
        return f"{self.customer.username}'s {self.get_asset_type_display()}"

    def clean(self):
        if self.asset_type == 'FD':
            if (self.purchase_price is not None or self.shares is not None or self.equity_symbol is not None):
                raise ValidationError("For Fixed Deposit, do not enter purchase price or shares or equity symbol.")
            if (self.maturity_date is None or self.principal_amount is None):
                raise ValidationError("Maturity date is required for Fixed Deposits.")
        elif self.asset_type == 'Equity':
            if (self.purchase_price is None or self.shares is None or self.equity_symbol is None):
                raise ValidationError("For Equity Investment, enter purchase price and shares and equity symbol.")
            if (self.maturity_date is not None or self.principal_amount is not None):
                raise ValidationError("For Equity Investment, do not enter principal amount and maturity date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

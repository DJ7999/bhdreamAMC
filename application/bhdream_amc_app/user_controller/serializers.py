from rest_framework import serializers
from .models import UserProfile, Investment, EquitySymbol
from django.contrib.auth.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_type']

class EquitySymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquitySymbol
        fields = ['id', 'symbol']

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'customer', 'asset_type', 'principal_amount', 'purchase_price', 'shares', 'investment_date', 'maturity_date', 'equity_symbol']


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['first_name', 'last_name', 'username', 'email', 'password']

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['username', 'password']
    def run_validation(self, data):
        return data


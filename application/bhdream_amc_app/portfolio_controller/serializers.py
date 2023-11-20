from rest_framework import serializers
from .models import Investment,Equity

class EquitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Equity
        fields = ['id','title', 'symbol']

class GetEquitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Equity
        fields = ['id','title', 'symbol','price']

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'user', 'equity', 'investment_date', 'shares', 'purchase_price']





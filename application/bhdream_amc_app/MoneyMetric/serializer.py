from rest_framework import serializers
from moneymetric.dto import EquityDTO, PortfolioDTO

class EquityDTOSerializer(serializers.Serializer):
    equity_symbol = serializers.CharField(max_length=10)
    amount_invested = serializers.FloatField()

class PortfolioDTOSerializer(serializers.Serializer):
    equities = EquityDTOSerializer(many=True)

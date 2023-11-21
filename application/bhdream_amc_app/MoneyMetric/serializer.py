from rest_framework import serializers
from .dto import EquityDTO, PortfolioDTO


class EquityDTOSerializer(serializers.Serializer):
    equity_symbol = serializers.CharField()
    amount_invested = serializers.DecimalField(max_digits=10, decimal_places=2)
    cagr = serializers.FloatField(allow_null=True)
    risk = serializers.FloatField(allow_null=True)
    optimal_weight = serializers.FloatField(allow_null=True)
    new_price=serializers.FloatField(allow_null=True)
    shares=serializers.IntegerField(allow_null=True)

class PortfolioDTOSerializer(serializers.Serializer):
    equities = EquityDTOSerializer(many=True)
    has_metrics = serializers.BooleanField()
    is_optimised = serializers.BooleanField()
    current_return = serializers.FloatField(allow_null=True)
    current_risk = serializers.FloatField(allow_null=True)
    optimised_return = serializers.FloatField(allow_null=True)
    optimised_risk = serializers.FloatField(allow_null=True)
    total_portfolio_value = serializers.DecimalField(max_digits=10, decimal_places=2)

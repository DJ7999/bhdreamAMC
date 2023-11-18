from rest_framework import serializers
from .models import Goal, FIRE

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'name', 'duration_in_months', 'monthly_contribution', 'goal_amount', 'is_active', 'active_date']

class FIRESerializer(serializers.ModelSerializer):
    class Meta:
        model = FIRE
        fields = ['id', 'user', 'duration', 'expected_inflation', 'todays_yearly_requirement', 'FIRE_amount', 'monthly_contribution']

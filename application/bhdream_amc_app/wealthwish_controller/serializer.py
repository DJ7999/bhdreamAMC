from rest_framework import serializers
from .models import Goal, FIRE

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'name', 'duration_in_months', 'monthly_contribution', 'goal_amount', 'is_active', 'active_date']

class FIREResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIRE
        fields = ['user', 'duration', 'todays_yearly_requirement', 'FIRE_amount', 'expected_inflation']

class FIRERequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIRE
        fields = ['user', 'duration', 'todays_yearly_requirement']


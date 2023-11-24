from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    duration_in_months = models.PositiveIntegerField()
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    active_date = models.DateField(null=True, blank=True)

class FIRE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    expected_inflation = models.DecimalField(max_digits=5, decimal_places=2, default=6.0)
    todays_yearly_requirement = models.DecimalField(max_digits=10, decimal_places=2)
    FIRE_amount = models.DecimalField(max_digits=10, decimal_places=2)


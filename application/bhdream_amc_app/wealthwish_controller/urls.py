from django.urls import path
from .views import GoalView,ActivateGoalView,FIREView

urlpatterns = [
    path("goals/",GoalView.as_view()),
    path("activate_goals/",ActivateGoalView.as_view()),
    path("FIRE/",FIREView.as_view()),       
]
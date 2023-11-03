#from .views import signin,signup
from django.urls import path,include
from .views import UserProfileView,UserView,EquitySymbolView,InvestmentView,SignInView,SignUpView,ProtectedResourceView
from django.contrib.auth.models import User

urlpatterns = [
    path("signin/",SignInView.as_view()),
    path("signup/",SignUpView.as_view()),
    path("user",ProtectedResourceView.as_view()),
    path("user_profile",UserProfileView.as_view()),
    path("equity_symbol",EquitySymbolView.as_view()),
    path("investment",InvestmentView.as_view()),
]

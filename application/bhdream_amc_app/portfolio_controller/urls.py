from django.urls import path,include
from .views import EquityView,InvestmentView,PortfolioView,PortfolioOptimizationView

urlpatterns = [
    path("equities/",EquityView.as_view()),
    path("investment/",InvestmentView.as_view()),   
    path("get_portfolio/",PortfolioView.as_view()),  
    path("get_optimised_portfolio/",PortfolioOptimizationView.as_view()),      
]

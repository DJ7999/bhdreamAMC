from django.urls import path,include
from .views import EquityView,InvestmentView

urlpatterns = [
    path("equities/",EquityView.as_view()),
    path('equities/<slug:symbol>/', EquityView.as_view()),
    path("investment/",InvestmentView.as_view()),   
]

#from .views import signin,signup
from django.urls import path,include
# from .views import UserProfileView,UserView,EquitySymbolView,InvestmentView,SignInView,SignUpView,ProtectedResourceView,
from .views import UserListView,SignInView,SignUpView,UpdateUserRoleView
from django.contrib.auth.models import User

urlpatterns = [
    path("signin/",SignInView.as_view()),
    path("signup/",SignUpView.as_view()),
    path("update_user_role/",UpdateUserRoleView.as_view()),
    path("",UserListView.as_view()),
    path('<int:user_id>/', UserListView.as_view())
]

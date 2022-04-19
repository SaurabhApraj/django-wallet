from django.urls import path
from .views import *

urlpatterns = [
    path('', homePage, name="dashboard"),
    path('login/', userlogin, name="login"),
    path('register/', userSignup, name="register"),
    path('logout/', userlogout, name="logout"),
    path('check-balance/', checkBalance, name="check_balance"),
    path('update-balance/', updateBalance, name="update_balance"),
    path('signup/', registerUser, name="signup"),
]
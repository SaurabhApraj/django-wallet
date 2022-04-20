from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="dashboard"),
    path('login/', user_login, name="login"),
    path('signup/', user_signup, name="signup"),
    path('logout/', user_logout, name="logout"),
    path('check-balance/', balance_check, name="check_balance"),
    path('update-balance/', balance_update, name="update_balance"),
    path('register/', register_user, name="register"),
]
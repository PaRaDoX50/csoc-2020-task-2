from django.urls import path
from authentication.views import *

urlpatterns = [
    
    path('signup/',registerView, name='user-signup'),
    path('login/',loginView, name='user-login'),
    path('logout/',logoutView, name='user-logout'),
]

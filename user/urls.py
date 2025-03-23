from django.urls import path
from .views import user_login, user_logout, user_delete, user_update, singup

urlpatterns = [
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('delete', user_delete, name='delete'),
    path('update', user_update, name='update'),
    path('signup', singup, name='signup'),
]
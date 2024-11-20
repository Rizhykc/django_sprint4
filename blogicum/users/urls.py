from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.UserloginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(),
         name='registration'),
    path('logout/', views.logout, name='logout'),
]
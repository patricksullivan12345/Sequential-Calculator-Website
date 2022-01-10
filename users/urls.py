from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('delete_profile/', views.deleteProfile, name="delete_profile"),
    path('edit_profile/', views.editAccount, name="edit_profile"),
    path('view_profile/', views.user_profile, name="view_profile"),

]
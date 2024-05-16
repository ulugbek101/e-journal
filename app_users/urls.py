from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update-profile/', views.update_profile_information, name='update_profile'),
    path('update-password/', views.update_profile_password, name='update_password'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),

    # API call
    path('update-attendance/', views.update_attendance),
    path('update-grades/', views.update_grades),
]

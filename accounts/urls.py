from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('backend/profile_settings/', views.profile_settings, name='profile_settings'),
    path('backend/profile_settings/upload/', views.profile_picture_upload, name='profile_picture_upload'),
    path('backend/profile_settings/remove/', views.profile_picture_remove, name='profile_picture_remove'),
    path('backend/profile_settings/user_update/', views.user_update, name='user_update'),
    path('backend/profile_settings/profile_update/', views.profile_update, name='profile_update'),
    path('backend/profile_settings/password_change/', views.password_change, name='password_change'),
    path('profile/password-changed/', TemplateView.as_view(
    template_name='accounts/password_change_success.html'
), name='password_change_success'),
]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pw_reset_form.html'), name='password_reset_confirm'),
    path('reset/done/', views.resetOk, name='password_reset_complete'),
]

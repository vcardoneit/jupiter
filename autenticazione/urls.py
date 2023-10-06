from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset_pw.html', html_email_template_name='pw_reset_email.html', subject_template_name="pw_reset_email_subjet.txt"), name='password_reset'),
    path('password_reset/done/', views.requestOk, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pw_reset_form.html'), name='password_reset_confirm'),
    path('reset/done/', views.resetOk, name='password_reset_complete'),
]
